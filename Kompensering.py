#!/usr/bin/python
# -*- coding: utf-8 -*-


class Kompensering:
    '''Kompensering är en klass som används
    för utekompensering. Man får sätta lite olika
    brytpunkter med SetVarden metoden, sätta MinMax
    och sen kör CountSP med utetemperaturen för att få
    tillbaka ett börvärde
    '''
    def __init__(self):
        self.DictVarden = {}
        self.SortedDictVarden = {}
        self.IterValue = 0

    def SetVarden(self, GraderUte, GraderFram):
        """SetVarden takes two values, the temperature outside,
        and the setpoint temperature for the shunt and puts them in a dict"""

        if isinstance(GraderUte, (int, float, complex)) and isinstance(GraderFram, (int, float, complex)):
            self.DictVarden[GraderUte] = GraderFram
        else:
            print('Wrong value!')

    def SetMin(self, Min):
        """Set max temperature out from shunt"""
        self.Min = Min

    def SetMax(self, Max):
        """Set min temperature out from shunt"""
        self.Max = Max

    def MinMax(self, Value):
        """MinMax returns a value between the set min and max values"""
        return max(self.Min, min(self.Max, Value))

    def CountSP(self, PV):
        """Calculate the actual setpoint based on the provided values and the
        actual outsidetemperature"""
        #Sort values

        self.SortedList = sorted(self.DictVarden.keys())
        self.IterValue = 0
        #Loop through outtemperature
        for i in sorted(self.DictVarden.keys()):
            #Find nearest upper value
            if i > PV:
                self.UpperValueKomp = i
                #take neares value under
                self.LowValueKomp = self.SortedList[self.IterValue-1]
                #finish
                break
            self.IterValue += 1
            if self.IterValue == len(self.DictVarden):
                return self.MinMax(self.DictVarden[self.SortedList[-1]])
        if self.UpperValueKomp == self.LowValueKomp:
            #if they are equal, assume the bottom was reached
            return self.MinMax(self.DictVarden[self.UpperValueKomp])
        self.y2 = self.DictVarden[self.UpperValueKomp]
        self.y1 = self.DictVarden[self.LowValueKomp]
        self.x2 = self.UpperValueKomp
        self.x1 = self.LowValueKomp
        #straight line equation
        self.k = (self.y2 - self.y1) / (self.x2 - self.x1)
        self.m = self.y1 - (self.x1 * self.k)
        self.SP = (PV * self.k) + self.m
        return self.MinMax(self.SP)


def main():
    Komp = Kompensering()
    Komp.SetVarden(20, 17)
    Komp.SetVarden(-10, 60)
    Komp.SetVarden(0, 55)
    Komp.SetVarden(10, 30)
    Komp.SetVarden(-20, 65)
    Komp.SetMax(65)
    Komp.SetMin(20)
    print(Komp.CountSP(-52))
    print(Komp.CountSP(152))


if __name__ == '__main__':
    main()
