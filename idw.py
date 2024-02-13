#Interpolace IDW
#Theodor Balek, 2.BGEKA
#Uvod do programovani

import math

class vstup():
    def __init__(self, file):
        self.__ipoints = []
        with open(file, "r", encoding="ASCII") as points:
            for i in points.readlines():
                self.__coordinates = i.strip().split(";")
                self.__ipoints.append(self.__coordinates)           #ze vstupniho souboru program vytvori seznam obsahujici body jako seznamy [id, x, y, z]
        self.__points = []
        for p in self.__ipoints:
            self.__points.append(list(map(float, p)))               #prevod vstupnich hodnot na datovy typ float

    def getpoints(self):
        return self.__points

    def vstupPrint(self):
        c = 0
        print("input points:")
        for j in self.__points:
            print(" x=", (self.__points[c][1]), ", y=", (self.__points[c][2]), ", z=", (self.__points[c][3]), sep="")
            c += 1

class point():
    def __init__(self, file, x = 0, y = 0, power = 2):          #trida bod pro zadani bodu o nezname souraznici z
        self.__file = file
        self.__x = x
        self.__y = y
        self.__power = power                                    #koeficient, na nejz se umocnuje vzdalenost pro vypocet vahy jednotlivych bodu
        if point.isnumber(self.__x) == False:
            raise TypeError("input x is not a number")
        if point.isnumber(self.__y) == False:
            raise TypeError("input y is not a number")
        if self.__power.isnumeric() == False:
            raise ValueError("input power is not positive integer")
        if int(self.__power) < 1:
            raise ValueError("input power should be at least 1")    #kontrola, zda jsou vstupni hodnoty spravne zadane

    def isnumber(a):
        try:
            float(a)
            return True
        except ValueError:
            return False

    def orientation(p1, p2, p3):                                        #vypocet zmeny „lomu” usecky
        x1,y1,x2,y2,x3,y3 = p1[1], p1[2], p2[1], p2[2], p3[1], p3[2]
        d = (y3-y2)*(x2-x1) - (y2-y1)*(x3-x2)                           #upravena funkce tg; rozdil uhlu s osou x
        if d > 0:
            return 1            #usecka se „lame doleva”
        elif d < 0:
            return -1           #usecka se „lame doprava”
        else:
            return 0            #usecka zustava ve stejnem smeru

    def calc_z(self):
        self.__w = 0                        #soucet vah jednotlivych bodu
        self.__zet = 0                      #hledana z souradnice
        self.__vst = vstup(self.__file)     #nacteni bodu ze vstupniho souboru
        self.__vst.vstupPrint()
        self.__cond = 0                     #parametr pro podminku, kdy uzivatel zada bod, ktery je ve vstupnich datech
        for q in self.__vst.getpoints():
            if (float(q[1]) != float(self.__x)) or (float(q[2]) != float(self.__y)):
                self.__cond = 1
            else:
                self.__cond = 0             #pokud uzivatel zada znamy body, pak program vypise jeho presnou hodnotu bez vypoctu
                self.__zet = float(q[3])
                break
        if self.__cond == 1:                #pokud uzivatel zada neznamy bod, pokracuje vypocet metodou IDW
            for (id,x,y,z) in (i for i in self.__vst.getpoints()):
                self.__w += 1/(((((float(x) - (float(self.__x)))**2)+((float(y)-(float(self.__y)))**2))**(1/2))**int(self.__power))     #vaha kazdeho bodu podle vzdalenosti umocnene na koeficient power
            for (id,x,y,z) in (i for i in self.__vst.getpoints()):
                self.__zet += ((1/(((((float(x) - (float(self.__x)))**2)+((float(y)-(float(self.__y)))**2))**(1/2))**int(self.__power)))/self.__w)*float(z)     #souradnice z jako suma dilcich vysek
        print("z_coordinate:", float(self.__zet))
        #poloha bodu vzhledem ke konvexni obalce vstupnich dat:
        self.__points = self.__vst.getpoints()
        self.__points.append([int(0), float(self.__x), float(self.__y), float(self.__zet)])     #pridani bodu ke vstupnim datum
        for k in range(len(self.__points)):                             #razeni bodu dle souradnice y
            for j in range(len(self.__points)-1):
                if self.__points[j][2] > self.__points[j+1][2]:
                    greater = self.__points[j]
                    self.__points[j] = self.__points[j+1]
                    self.__points[j + 1] = greater
        self.__p0 = self.__points[0]            #p0 - bod s nejnizsi souradnici y
        for p in self.__points[1::]:            #vypocet uhlu polarnich souradnic kazdeho bodu vzhledem k p0
            if p[1] >= self.__p0[1]:
                angle = math.atan((p[2]-self.__p0[2])/(p[1]-self.__p0[1]))
            else:
                angle = math.radians(180) - abs(math.atan((p[2]-self.__p0[2])/(p[1]-self.__p0[1])))
            p.append(angle)                     #pridani uhlu do seznamu informaci o bodu [id, x, y, z, uhel]
        for j in range(len(self.__points)-1):       #razeni bodu podle uhlu
            for p in range(len(self.__points)-2):
                if self.__points[p+1][4] > self.__points[p+2][4]:
                    greater = self.__points[p+1]
                    self.__points[p+1] = self.__points[p+2]
                    self.__points[p+2] = greater
                elif self.__points[p+1][4] == self.__points[p+2][4]:        #pokud maji dva body stejny uhel, pak razeni dle vzdalenosti od p0
                    if math.dist(self.__p0[1:3:], self.__points[p+1][1:3:]) > math.dist(self.__p0[1:3:], self.__points[p+2][1:3:]):
                        greater = self.__points[p+1]
                        self.__points[p+1] = self.__points[p+2]
                        self.__points[p+2] = greater
        for a in self.__points[1::]:
            a.pop(4)                    #vyjmuti informace o uhlu ze seznamu bodu pro pozdejsi porovnani - bod opet [id, x, y, z]
        self.__hull = []                #list, ktery bude obsahovat body tvorici okraj konvexni obalky
        for i in range(len(self.__points)):
            while len(self.__hull) >= 2 and point.orientation(self.__hull[-2], self.__hull[-1], self.__points[i]) != 1:     #urceni konvexni obalky podle orientace bodu
                self.__hull.pop()
            self.__hull.append(self.__points[i])
        if [int(0), float(self.__x), float(self.__y), float(self.__zet)] in self.__hull and self.__cond == 1:   #pokud hledany bod je soucasti okraje konvexni obalky, pak jde o extrapolaci
            print("EXTRAPOLATION - point is out of the convex hull")
        else:                                                                                                   #pokud hledany bod neni soucasti okraje konvexni obalky, pak jde o interpolaci
            print("INTERPOLATION - point is in the convex hull")

q = point(input("path: "), input("x:"),input("y:"),input("power:"))
q.calc_z()