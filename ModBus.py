#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymodbus3.client.sync import ModbusTcpClient
from ModbusDigitalInputIOCardClass import ModbusDigitalInputIOCard
from ModbusDigitalOutputIOCardClass import ModbusDigitalOutputIOCard

#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

def runModBus(IOVariables):
    #---------------------------------------------------------------------------#
    # choose the client you want
    #---------------------------------------------------------------------------#
    # make sure to start an implementation to hit against. For this
    # you can use an existing device, the reference implementation in the tools
    # directory, or start a pymodbus server.
    #---------------------------------------------------------------------------#
    client = ModbusTcpClient('192.168.1.9')
    #rq = client.write_registers(2048, [0])
    #rr = client.read_input_registers(000, 1)
    #print (rr.registers)       
    #---------------------------------------------------------------------------#
    # configure io card
    #---------------------------------------------------------------------------#
    #Digital_In_1 = ModbusDigitalInputIOCard(0, client)   
    #print('IOVariables in modbus.py: {IOVariables} '.format(IOVariables=IOVariables))  
    Digital_Out_1 = ModbusDigitalOutputIOCard(2048, client, IOVariables)          
    #---------------------------------------------------------------------------#
    # Run io card
    #---------------------------------------------------------------------------#
    #Digital_In_1.ReadStatus()
    #---------------------------------------------------------------------------#
    # Run io card
    #---------------------------------------------------------------------------#
    Digital_Out_1.WriteStatus()
    #---------------------------------------------------------------------------#
    # close the client
    #---------------------------------------------------------------------------#
    client.close()      






