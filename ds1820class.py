#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import os
import sqlite3 as lite


class DS1820():
    '''Class for woking with a DS1820 temperature sensor
    '''

    def __init__(self, address):
        """Some initialization		"""
        self.adress = address
        self.temp = 0.0
        self.interval = 0.0
        self.HighAlarmActivated = False
        self.LowAlarmActivated = False
        self.timestamp = 0
        self.data_string = ''
        self.trend_func = Write_temp(self.temp, self.adress)
        self.Name = ''
        self.Comment = ''

    def SetWriteInterval(self, interval):

        'Can be removed, not needed, logging is in its own class'
        self.interval = interval
        return self.interval

    def SetHighThreshold(self, HighThreshold):
        self.HighAlarmActivated = True
        self.HighAlarmTreshold = HighThreshold
        return self.HighAlarmTreshold

    def SetLowThreshold(self, LowThreshold):
        self.LowAlarmActivated = True
        self.LowAlarmTreshold = LowThreshold
        return self.LowAlarmTreshold

    def CheckTemperatureAlarm(self):
        '''Checks whether any alarm are activated, if they are
        Check if they are higher/lower than the threshold, if they are
        set the alarm'''
        if self.LowAlarmActivated:
            if self.temp < self.LowAlarmTreshold:
                self.LowAlarm = True
        else:
            self.LowAlarm = False

        if self.HighAlarmActivated:
            if self.temp > self.HighAlarmTreshold:
                self.HighAlarm = True
        else:
            self.HighAlarm = False

    def ReadTemp(self):
        '''Read the file that stores temperature data, use the folder
        with the provided adress. Dont forget to run modprobe on the pi'''
        with open(r'/sys/bus/w1/devices/' + self.adress + r'/w1_slave', 'r') as tempfile:
            data = tempfile.read()  # Read the whole file
            if 'YES' in data:
                temp_pos = data.find('t=')  # Look for t, this is where the temperature is
                data = data[temp_pos + 2:]  # remove 't='
                data = float(data) / 1000  # insert comma,
                self.temp = data
                return data

    def RunMainTemp(self):
        '''This is where the magic happens'''
        self.ReadTemp()

        self.CheckTemperatureAlarm()

        # self.Write_temp2()
        self.trend_func.value = self.temp
        self.trend_func.main()

        return self.temp


class Write_temp():
    ''' A class that writes the actual value and time into a file
    that changes every 24 hours
    Value of the signal and name that is should be stored'''

    def __init__(self, value, name):
        self.path = '/home/pi/Projects/Home-automation/sensors/' + str(name) + '/'
        self.value = value
        self.file_date = int(time.time())
        self.name = name
        self.name_dikt = {
            '28-00000523a1cb': 'VS1_GT1',
            '28-00000524056e': 'VS1_GT2',
            '28-0000052407e0': 'VS1_GT3',
            '28-00000523ab8e': 'SUN_GT1',
            '28-0000052361be': 'SUN_GT2'}

    def SQL_main(self):
        conn = lite.connect('data.db')
        with conn:
            cur = conn.cursor()

            #If the key doesnt exist, create one
            if self.name in self.name_dikt:
                pass
            else:
                self.name_dikt[self.name] = [self.name]

            #Check if the column exists, if it doesnt create a new one
            try:
                cur.execute('select * from {}'.format(
                    str(self.name_dikt[self.name])))
            except lite.OperationalError:
                cur.execute('''
                    CREATE TABLE {} (Time TEXT, Temp REAL)'''.format(
                            str(self.name_dikt[self.name])))

            cur.execute("INSERT INTO " + str(self.name_dikt[self.name]) + " VALUES(?,?)", (int(time.time()), str(self.value)))

    def main(self):
        if self.file_date < time.time() - 86400:
            # if the file_date is more than 24 hours old, make a 'new' file date with actual time
            self.file_date = int(time.time())
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(self.path + str(self.file_date), 'a+') as outfile:
            outfile.write(str(int(time.time())) + '|' + str(self.value) + '\n')
        self.SQL_main()



class DegreeDays(object):
    """docstring for ClassName
    This class shall store todays temperature, one log per minute 
    and then calculate the median and then calculate the amount of 
    DegreeDays


    """
    def __init__(self, temp):
        self.TodaysTemp = temp
        self.temp_dict = {
            1: 17,
            2: 17,
            3: 17,
            4: 12,
            5: 10,
            6: 10,
            7: 10,
            8: 11,
            9: 12,
            10: 13,
            11: 17,
            12: 17,
        }

def DegreeDays():
    ''' A function that once a day calculate the median temperature of today and the amount
    of DegreeDays returned are the "17 - median temperature" '''
    # MedianTemperature =
    pass
