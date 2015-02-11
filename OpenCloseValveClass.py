#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Timer
import datetime as dt


class OpenCloseValve(object):
    'A class that controls a valve with a close and a open signal'
    def __init__(self):
        self.deadband = 2.0
        self.Man_Open = False
        self.Man_Close = False
        self.Man_Close_OUT = False
        self.Man_Open_OUT = False
        self.Name = 'Default_valve_name'
        self.Open_IO = 'Default_valve_name_Open'
        self.Close_IO = 'Default_valve_name_Close'
        self.Time_Open = 3.0  # Seconds the valve shall open
        self.Time_Close = 3.0  # Seconds the valve shall close

    def man(self, direction, io_dict):
        #self.WriteDoc(direction)
        if direction == 'open':
            #Set variable
            io_dict[self.Open_IO]['Value'] = True
            self.OpenTimer = Timer(
                self.Time_Open,
                self.SetIOdict,
                [self.Open_IO, False, io_dict]
                )
            #Reset variable after timer is finished
            self.OpenTimer.start()
        elif direction == 'close':
            #Set variable
            io_dict[self.Close_IO]['Value'] = True
            self.CloseTimer = Timer(
                self.Time_Close,
                self.SetIOdict,
                [self.Close_IO, False, io_dict]
                )
            #Reset variable after timer is finished
            self.CloseTimer.start()

    def SetIOdict(self, io, value, io_dict):
        io_dict[io]['Value'] = value

    def WriteDoc(self, msg):
        with open('Docs/{}'.format(self.Name), 'a+') as f:
            f.write('Time: {}, direction: {} \n'.format(
                dt.datetime.now(),
                msg
                )
            )

    def main(self, PV, SP, io_dict):
        '''In this method the temperatures
        are compared, and some control variables
        are set for later activaion of the IO
        '''
        self.deltaT = SP - PV
        if (self.deadband < self.deltaT
                and not io_dict[self.Close_IO]['Value']):
            'If deltaT is bigger than the deadband, open valve and Heat'
            #Open
            self.man('open', io_dict)
        elif (self.deltaT < 0 - self.deadband
                and not io_dict[self.Open_IO]['Value']):
            '''If deltaT is less than 0 minus deadband,
            close valve and Dont heat'''
            #close
            self.man('close', io_dict)
