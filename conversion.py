#Conversion of a number from binary system to decimal system and back
#Theodor Balek, 2.BGEKA
#Introduction to programming

class bin():
    counter = 1
    def __init__(self, a = 0.0):
        b = {"0", "1", "."}                                                 #set of symbols that can be used by a binary number
        if set(str(a)).issubset(b) == False or bin.isnumber(a) == False:    #test if the input number is binary
            raise TypeError("number is not positive binary")
        if float(a) <= 0:                                                   #test if the input number is positive
            raise ValueError("number is not positive")
        self.__id = bin.counter
        self.__a = float(a)
        if {"."}.issubset(set(str(a))):                #dividing the input number into an integer (self.__n) and decimal (self.__m) part
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

    def to_dec(self):                               #conversion of the number from binary to decimal system
        self.__d = 0
        p = -(len(self.__m))                        #a power is equal to an opposite value of a length of the decimal part of the input number
        for i in self.__m[::-1]:
            self.__d += int(i) * (2**p)
            p += 1
        for j in self.__n[::-1]:
            self.__d += int(j) * (2**p)             #raise number 2 to the power; e.g. 2**(0) + 2**(1) + 2**(2)
            p += 1                                  #the power is increased by 1 in each iteration
        print(" dec from bin: "+str(self.__d))

    def to_bin(self):                               #conversion back to the decimal system
        self.__N = []                               #integer part of a binary form
        self.__f = self.__d % int(self.__d)         #decimal part of a decimal form
        self.__M = []                               #decimal part of a binary form
        while int(self.__d) >= 2:                   #calculation of an integer part by division by 2 successively
            self.__N.append(int(self.__d)%2)
            self.__d = int(self.__d) // 2
        self.__N.append(int(self.__d%2))
        for k in range(len(self.__m)):              #calculation of a decimal part by multiplication by 2 successively
            self.__M.append(int(self.__f*2))        #the programme writes 0 or 1 according to the result of a double of decimal part of decimal form
            if int(self.__f*2) == 0:                #adjustment of a decimal part while exceeding a 1
                self.__f = self.__f*2
            else:
                self.__f = (self.__f*2) % int(self.__f*2)
        print(" bin from dec: ", *self.__N[::-1], ".", *self.__M[::], sep="")

a = bin(input("bin_num: "))
a.print()
a.to_dec()
a.to_bin()