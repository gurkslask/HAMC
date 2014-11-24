#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2

def GetData():
    #Open forecast homepage
    res = urllib2.urlopen('http://www.temperatur.nu/kalmar-prognos.html')
    #read the data
    data = res.read()

    #Find start position
    start_pos=data.find('width="38" alt=')
    if start_pos != -1:
        #From start position, find end position
        end_pos=data[start_pos:].find('" style') + start_pos
        #Here we have our string
        forecast=data[start_pos+16:end_pos]
    else:
        forecast = 'None'

    return forecast





if __name__ == '__main__':
    print(GetData())
