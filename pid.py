#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AdministratÃ¶r
#
# Created:     11-09-2013
# Copyright:   (c) AdministratÃ¶r 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time

class PID:
    """ Simple PID control.

        This class implements a simplistic PID control algorithm. When first
        instantiated all the gain variables are set to zero, so calling
        the method GenOut will just return zero.
    """
    def __init__(self):
        # initialze gains
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        self.OutMax = 100.0
        self.OutMin = 0.0

        self.Initialize()

    def SetKp(self, invar):
        """ Set proportional gain. """
        self.Kp = invar

    def SetKi(self, invar):
        """ Set integral gain. """
        self.Ki = invar

    def SetKd(self, invar):
        """ Set derivative gain. """
        self.Kd = invar

    def SetPrevErr(self, preverr):
        """ Set previous error value. """
        self.prev_err = preverr

    def SetOutMax(self, Max):
        """ Set Max output, default 100.0 """
        self.OutMax = Max

    def SetOutMin§(self, Min):
        """ Set Min output, default 0.0 """
        self.OutMin = Min


    def Initialize(self):
        # initialize delta t variables
        self.currtm = time.time()
        self.prevtm = self.currtm

        self.prev_err = 0

        # term result variables
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0


    def GenOut(self, error):
        """ Performs a PID computation and returns a control value based on
            the elapsed time (dt) and the error signal from a summing junction
            (the error parameter).
        """
        self.currtm = time.time()               # get t
        dt = self.currtm - self.prevtm          # get delta t
        de = error - self.prev_err              # get delta error

        self.Cp = self.Kp * error               # proportional term
        self.Ci += error * dt                   # integral term

        self.Cd = 0
        if dt > 0:                              # no div by zero
            self.Cd = de/dt                     # derivative term

        self.prevtm = self.currtm               # save t for next pass
        self.prev_err = error                   # save t-1 error

        # sum the terms and return the result
        return min(self.OutMax, max(self.OutMin, self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)))

def main():
    pid = PID()
    pid.SetKp(10)
    pid.SetKi(1)
    pid.SetKd(1)
    for i in range(100):
        print(pid.GenOut(2.2))
        time.sleep(0.4)

if __name__ == '__main__':
    main()