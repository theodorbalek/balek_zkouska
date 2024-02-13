#Prevod cisla z dvojkove do desitkove soustavy a zpet
#Theodor Balek, 2.BGEKA
#Uvod do programovani

class bin():
    counter = 1
    def __init__(self, a = 0.0):
        b = {"0", "1", "."}                                                 #mnozina znaku, ktere muze obsahovat binarni cislo
        if set(str(a)).issubset(b) == False or bin.isnumber(a) == False:    #test, zda je vstupni cislo binarni
            raise TypeError("number is not positive binary")
        if float(a) <= 0:                                                   #test, zda je vstupni cislo kladne
            raise ValueError("number is not positive")
        self.__id = bin.counter
        self.__a = float(a)
        if {"."}.issubset(set(str(a))):                #rozdeleni vstupniho cisla na celou a desetinnou cast (n a m)
            self.__n = [*(str(a).split(".")[0])]
            self.__m = [*(str(a).split(".")[1])]
        else:
            self.__n = [*(str(a).split(".")[0])]
            self.__m = [str(0)]
        bin.counter += 1

    def isnumber(a):
        try:
            float(a)
            return True
        except ValueError:
            return False

    def print(self):
        print ("ID: ", str(self.__id), "\n bin_number: ", self.__a, "\n integer: ", "".join(self.__n), "\n decimal: ", "".join(self.__m))

    def to_dec(self):                               #prevod cisla z dvojkove do desitkove soustavy
        self.__d = 0
        p = -(len(self.__m))                        #exponent odpovida opacne hodnote delky desetinne casti vstupniho cisla
        for i in self.__m[::-1]:
            self.__d += int(i) * (2**p)
            p += 1
        for j in self.__n[::-1]:
            self.__d += int(j) * (2**p)
            p += 1                                  #exponent se v kazde iteraci zvetsi o 1; umocneni cisla 2 postupne napr. 2**(0) + 2**(1) + 2**(2)
        print(" dec from bin: "+str(self.__d))

    def to_bin(self):                               #prevod zpet do binarni soustavy
        self.__N = []                               #cela cast binarniho tvaru
        self.__f = self.__d % int(self.__d)         #desetinna cast decimalniho tvaru
        self.__M = []                               #desetinna cast binarniho tvaru
        while int(self.__d) >= 2:                   #vypocet cele casti postupnym delenim dvema
            self.__N.append(int(self.__d)%2)
            self.__d = int(self.__d) // 2
        self.__N.append(int(self.__d%2))
        for k in range(len(self.__m)):              #vypocet desetinne casti postupnym nasobenim dvema
            self.__M.append(int(self.__f*2))        #program zapise 0, nebo 1 podle vysledku dvojnasobku desetinne casti desitkoveho tvaru
            if int(self.__f*2) == 0:                #uprava desetinne casti pri prekroceni radu
                self.__f = self.__f*2
            else:
                self.__f = (self.__f*2) % int(self.__f*2)
        print(" bin from dec: ", *self.__N[::-1], ".", *self.__M[::], sep="")

a = bin(input("bin_num: "))
a.print()
a.to_dec()
a.to_bin()