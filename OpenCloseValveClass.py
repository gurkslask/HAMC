#!/usr/bin/python
# -*- coding: utf-8 -*-
from ds1820class import Write_temp
import time
import datetime as dt
from threading import Timer


def Documentation(state):
    with open('valve', 'a+') as f:
        f.write(state)


class OpenCloseValve(object):
    'A class that controls a valve with a close and a open signal'
    def man(self, tag, value):
        tag = value
        self.Documentation(tag, value)
        return tag

    def Close(self):
        self.Man_Close_OUT = True
        self.CloseTimer = Timer(self.Time_Close, self.man, [self.Man_Close_OUT, False])
        self.CloseTimer.run()

    def Open(self):
        self.Man_Open_OUT = True
        self.OpenTimer = Timer(self.Time_Open, self.man, [self.Man_Open_OUT, False])
        self.OpenTimer.run()

    def __init__(self):
        self.deadband = 2.0
        self.Man_Open = False
        self.Man_Close = False
        self.Man_Close_OUT = False
        self.Man_Open_OUT = False
        self.Name = 'a'
        self.Time_Open = 3.0  # Seconds the valve shall open
        self.Time_Close = 2.0  # Seconds the valve shall close
        #Declar instances for logging
        #self.Write_Stat_Open = Write_temp(self.Man_Open, 'VS1_SV1_Open')
        #self.Write_Stat_Close = Write_temp(self.Man_Close, 'VS1_SV1_Close')

        self.Control_Time = 0
        self.Control_Active = False
        self.ControlTimeReset = time.time()

    def Documentation(self, direction, value):
        with open('Docs/' + self.Name, 'a+') as f:
            f.write('{} went {} {} at {}'.format(
                self.Name, direction, value, time.time()))

    def main(self, PV, SP):
        '''In this method the temperatures
        are compared, and some control variables
        are set for later activaion of the IO
        '''
        self.deltaT = SP - PV
        if self.deadband < self.deltaT:
            'If deltaT is bigger than the deadband, open valve and Heat'
            #Open
            self.Control_Active = True
            self.Man_Open = True
            self.Man_Close = False

        elif self.deltaT > 0 - self.deadband:
            '''If deltaT is less than 0 minus deadband,
            close valve and Dont heat'''
            #close
            self.Control_Active = True
            self.Man_Close = True
            self.Man_Open = False

        else:
            'If none is true, do nothing'
            self.Control_Active = False
            self.Man_Close = False
            self.Man_Open = False

    def control(self):
        '''Here the IO are controlled
        based on the control variables from
        main method
        '''
        #Can only run Control method once every 10 seconds

        if self.Man_Close and self.ControlTimeReset + 10 < time.time() and not self.Man_Open_OUT:
            #Run the Close method
            self.Close()
            #Reset the reset time so it only runs every 10 seconds
            self.ControlTimeReset = time.time()

        if self.Man_Open and self.ControlTimeReset + 10 < time.time() and not self.Man_Close_OUT:
            #Run the Open method
            self.Open()
            #Reset the reset time so it only runs every 10 seconds
            self.ControlTimeReset = time.time()



