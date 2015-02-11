#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.request import urlopen

def GetData():
    #Open forecast homepage
    res = urlopen('http://www.temperatur.nu/kalmar-prognos.html')
    #read the data
    data = str(res.read())

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
