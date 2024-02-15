#Interpolation IDW
#Theodor Balek, 2.BGEKA
#Introduction to programming

import math

class inpt():
    def __init__(self, file):
        self.__ipoints = []
        with open(file, "r", encoding="ASCII") as points:
            for i in points.readlines():
                self.__coordinates = i.strip().split(";")
                self.__ipoints.append(self.__coordinates)           #from input file create a list of points as lists [id, x, y, z]
        self.__points = []
        for p in self.__ipoints:
            self.__points.append(list(map(float, p)))               #conversion of input values to float type

    def getpoints(self):
        return self.__points

    def inptprint(self):
        c = 0
        print("input points:")
        for j in self.__points:
            print(" x=", (self.__points[c][1]), ", y=", (self.__points[c][2]), ", z=", (self.__points[c][3]), sep="")
            c += 1

class point():
    def __init__(self, file, x = 0, y = 0, power = 2):          #class point for inputting a point with unknown z coordinate
        self.__file = file
        self.__x = x
        self.__y = y
        self.__power = power                                    #a coefficient to which the distance is powered to calculate the weight of each point
        if point.isnumber(self.__x) == False:
            raise TypeError("input x is not a number")
        if point.isnumber(self.__y) == False:
            raise TypeError("input y is not a number")
        if self.__power.isnumeric() == False:
            raise ValueError("input power is not positive integer")
        if int(self.__power) < 1:
            raise ValueError("input power should be at least 1")    #tests if the input values are correctly inputted

    def isnumber(a):
        try:
            float(a)
            return True
        except ValueError:
            return False
        
    def calc_z(self):
        self.__w = 0                        #a sum of a weights of points
        self.__zet = 0                      #unknown coordinate
        self.__vst = inpt(self.__file)      #reading points from the input file
        self.__vst.inptprint()
        self.__cond = 0                     #parametr for condiotion when a user insert a point that is part of input points with known z coordinate
        for q in self.__vst.getpoints():
            if (float(q[1]) != float(self.__x)) or (float(q[2]) != float(self.__y)):
                self.__cond = 1
            else:
                self.__cond = 0             #if the user inserts known point, programme writes the exact value without a calculation
                self.__zet = float(q[3])
                break
        if self.__cond == 1:                #if the user inserts unknown point, the IDW calculation continues
            for (id,x,y,z) in (i for i in self.__vst.getpoints()):
                self.__w += 1/(((((float(x) - (float(self.__x)))**2)+((float(y)-(float(self.__y)))**2))**(1/2))**int(self.__power))     #weighting each point by the distance raised to the power coefficient
            for (id,x,y,z) in (i for i in self.__vst.getpoints()):
                self.__zet += ((1/(((((float(x) - (float(self.__x)))**2)+((float(y)-(float(self.__y)))**2))**(1/2))**int(self.__power)))/self.__w)*float(z)     #z coordinate is a sum of a partial heights
        print("z_coordinate:", float(self.__zet))    

    def orientation(p1, p2, p3):                                        #calculation of a refraction of a line segment
        x1,y1,x2,y2,x3,y3 = p1[1], p1[2], p2[1], p2[2], p3[1], p3[2]
        d = (y3-y2)*(x2-x1) - (y2-y1)*(x3-x2)                           #tangens function; difference of the angles with x axis
        if d > 0:
            return 1            #the line segment is "turning left"
        elif d < 0:
            return -1           #the line segment is "turning right"
        else:
            return 0            #the line segment keeps the direction

    def lowest_y(list):             #sort points by y coordinate
        for k in range(len(list)):
            for j in range(len(list)-1):
                if list[j][2] > list[j+1][2]:
                    greater = list[j]
                    list[j] = list[j+1]
                    list[j+1] = greater
        p0 = list[0]
        return p0       #return a point with the lowest y coordinate
    
    def sort_angle(list, p0):
        for j in range(len(list)-1):       #sort points by angle
            for p in range(len(list)-2):
                if list[p+1][4] > list[p+2][4]:
                    greater = list[p+1]
                    list[p+1] = list[p+2]
                    list[p+2] = greater
                elif list[p+1][4] == list[p+2][4]:        #if the angles are the same, sort by distance from p0
                    if math.dist(p0[1:3:], list[p+1][1:3:]) > math.dist(p0[1:3:], list[p+2][1:3:]):
                        greater = list[p+1]
                        list[p+1] = list[p+2]
                        list[p+2] = greater
        return list
    
    def convex(self):                               #position of the point according to the convex hull
        self.__points = self.__vst.getpoints()
        self.__points.append([int(0), float(self.__x), float(self.__y), float(self.__zet)])     #add the unknown point to input poits
        self.__p0 = point.lowest_y(self.__points)          #point with the lowest y coordinate
        for p in self.__points[1::]:            #calculating the angle of the polar coordinates of each point relative to p0
            if p[1] >= self.__p0[1]:
                angle = math.atan((p[2]-self.__p0[2])/(p[1]-self.__p0[1]))
            else:
                angle = math.radians(180) - abs(math.atan((p[2]-self.__p0[2])/(p[1]-self.__p0[1])))
            p.append(angle)                     #add the angle to informations about point [id, x, y, z, uhel]
        self.__points = point.sort_angle(self.__points, self.__p0)      #sort points by that angle
        for a in self.__points[1::]:
            a.pop(4)                    #remove the information about angle [id, x, y, z]
        self.__hull = []                #the list of a convex hull
        for i in range(len(self.__points)):
            while len(self.__hull) >= 2 and point.orientation(self.__hull[-2], self.__hull[-1], self.__points[i]) != 1:     #convex hull according to orientation of points
                self.__hull.pop()
            self.__hull.append(self.__points[i])
        if [int(0), float(self.__x), float(self.__y), float(self.__zet)] in self.__hull and self.__cond == 1:   #if the unknown point is part of a convex hull, it was an extrapolation
            print("EXTRAPOLATION - point is out of the convex hull")
        else:                                                                                                   #if the unknown point is not part of a convex hull, it was not an extrapolation
            print("INTERPOLATION - point is in the convex hull")

q = point(input("path: "), input("x:"),input("y:"),input("power:"))
q.calc_z()
q.convex()