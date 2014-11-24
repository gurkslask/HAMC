#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import time
import pickle


class PumpControl(object):
    '''The default PumpControl class'''

    def __init__(self, name=''):
        #The delay for alarms
        self.LarmDelay = 15
        #Set this from the program to make the pump go if in auto
        self.Man = False
        #Tie this signal to the actual output
        self.Out = False
        self.Comment = ''
        self.Name = name
        self.S1 = 0  #today
        self.S2 = 0  #yesterday
        self.S3 = 0  #total
        self.T1 = 0  #today
        self.T2 = 0  #yesterday
        self.T3 = 0  #total
        try:
            self.unpickla()
        except Exception, e:
            print('unpickla went wrong' + str(e))

    def Documentation(self):
        with open('Docs/' + self.Name, 'a+') as f:
            f.write('{} went {} at {}'.format(self.Name, self.Out, time.time()))

    def main(self, DI):
        if self.Man and not self.Out:
            self.Out = True
            self.S1 += 1
            self.S3 += 1
            self.Documentation()

        elif not self.Man and self.Out:
            self.Out = False

        if DI != self.Out:
            self.Larm = True
        else:
            self.Larm = False

        try:
            self.pickla()
        except Exception, e:
            print('pickla went wrong' + str(e))

    def NewDay(self):
        #move today to yesterday and reset today, DONT FORGET TO PUT THIS IN CHECKIFNEWDAY METHOD IN MAIN
        self.S2, self.S1 = self.S1, 0

    def pickla(self):
        with open(''.join(['pickles/', self.Name]), 'wb+') as p:
            pickle.dump(self.__dict__, p, 2)

    def unpickla(self):
        with open(''.join(['pickles/', self.Name]), 'rb') as p:
            self.__dict__ = pickle.load(p)

def Control_of_CP2(Weather, Out_temperature, Tank_temperature, Sun_heater_temperature):

    Weather_dict={
        'Heavy rain and thunder' : 7, # Kraftigt regn och aska
        'Rain showers' : 7, # Rain showers - regnskurar
        'Cloudy' : 7, # Cloudy - moln
        'Fair' : 5, # Fair - 75% sol
        'Partly cloudy' : 6, # Partly cloudy - 50 50
        'Clear sky' : 4, # Clear sky - soligt
        'Rain' : 7, # Rain - regn
        'None' : 7, # No info
        'Light rain' : 7 
    }

    try:
        hysteresis = Weather_dict[Weather]
    except:
        hysteresis = 7
        print('Bad weather string!{w}'.format(w=Weather))
    IOoutput=False
    if Sun_heater_temperature > Tank_temperature +  hysteresis:
        IOoutput = True
    elif Sun_heater_temperature < Tank_temperature:
        IOoutput = False
    return IOoutput

