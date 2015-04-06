#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ds1820class import DS1820, Write_temp
from Kompensering import Kompensering
from OpenCloseValveClass import OpenCloseValve
from IOdef import IOdef
from scraping import GetData
from PumpControl import PumpControl
from ModBus import runModBus
import time
import datetime as dt
import asyncio
from timechannel import timechannel
from socket_server import EchoServerClientProtocol


class MainLoop():
    def __init__(self):
        self.test_HAMC_Data = {'fyrtio': 40, 'tva': 2}
        self.socket_host = '127.0.0.1'
        self.socket_port = 5004
        self.loop = asyncio.get_event_loop()
        # Each client connection will create a new protocol instance
        self.coro = self.loop.create_server(
            lambda: EchoServerClientProtocol(self.data_func),
            self.socket_host,
            self.socket_port)
        self.server = self.loop.run_until_complete(self.coro)
        self.loop.create_task(self.async_5sec())
        self.loop.create_task(self.async_20sec())
        self.loop.create_task(self.async_1440sec())
        self.loop.create_task(self.async_3600sec())

        # Serve requests until CTRL+c is pressed


        # Declare IO Variables
        self.IOVariables = IOdef()

        # Declare temperaturecompensation
        self.Komp = Kompensering()
        self.Komp.SetVarden(20, 17)
        self.Komp.SetVarden(-10, 40)
        self.Komp.SetVarden(0, 35)
        self.Komp.SetVarden(10, 30)
        self.Komp.SetVarden(-20, 65)
        self.Komp.SetMax(65)
        self.Komp.SetMin(20)

        # Loggin of the compensation
        self.Setpoint_VS1 = 0.0
        self.Setpoint_Log_VS1 = Write_temp(self.Setpoint_VS1, 'VS1_Setpoint')

        # Declare temperature sensors
        # Framledning
        self.VS1_GT1 = DS1820('28-00000523a1cb')
        self.VS1_GT1.Comment = '''
        This is the sensor that measures
        the water temperature to the radiators'''
        self.VS1_GT1.Name = 'VS1_GT1'
        # Retur
        self.VS1_GT2 = DS1820('28-00000524056e')
        self.VS1_GT2.Comment = '''This is the sensor that measures
         the water temperature from the radiators'''
        self.VS1_GT2.Name = 'VS1_GT2'
        # Ute
        self.VS1_GT3 = DS1820('28-0000052407e0')
        self.VS1_GT3.Comment = '''This is the sensor that measures
         the outdoor temperature'''
        self.VS1_GT3.Name = 'VS1_GT3'
        # @Solar panels
        # self.SUN_GT1 = DS1820('28-00000523ab8e')
        # self.SUN_GT1.Comment = '''This is the sensor that measures
        # the water temperature to the solar panels'''
        # self.SUN_GT1.Name = 'SUN_GT1'
        # After solar panels
        self.SUN_GT2 = DS1820('28-0000052361be')
        self.SUN_GT2.Comment = '''This is the sensor that measures
         the water temperature from the solar panels'''
        self.SUN_GT2.Name = 'VS1_GT2'

        # Declare logging interval
        self.VS1_GT1.SetWriteInterval(60)
        self.VS1_GT2.SetWriteInterval(60)
        self.VS1_GT3.SetWriteInterval(60)
        # self.SUN_GT1.SetWriteInterval(60)
        self.SUN_GT2.SetWriteInterval(60)

        # Declare Heating valve
        self.VS1_SV1_Class = OpenCloseValve()
        self.VS1_SV1_Class.Name = 'VS1_SV1'
        self.VS1_SV1_Class.Open_IO = 'b_VS1_SV1_OPEN_DO'
        self.VS1_SV1_Class.Close_IO = 'b_VS1_SV1_CLOSE_DO'

        # Initialize the loops
        self.ActTimeLoop1 = time.time()
        self.ActTimeLoop2 = time.time()
        self.ActTimeLoop3 = time.time() - 14400
        self.ActTimeLoop4 = time.time()
        self.ActTimeLoop5 = time.time()

        # Declare Cirkulation pump sun heaters
        self.VS1_CP2_Class = PumpControl('SUN_P1')
        self.VS1_CP2_Class.Comment = '''This is the pump that pumps
         water up to the sun heaters'''
        # self.VS1_CP2_Class.Name='SUN_P1'

        # Declare Circualation pump for radiators in the house
        self.VS1_CP1_Class = PumpControl('VS1_CP1')
        self.VS1_CP1_Class.Comment = ('''This is the pump that supplies
         the heating radiators with hot water''')

        # Declare variebles
        self.Weather_State = ''
        self.exit_flag = False
        self.datumtid = dt.date.today()
        self.ThreeDayTemp = 9.0

        self.choice = False

        # Declare timechannel
        self.time_channel_VS1_SV1 = timechannel()
        self.VS1_SV1_SP_Down = False
        self.time_channel_VS1_SV1.time_dict[0] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.time_channel_VS1_SV1.time_dict[1] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.time_channel_VS1_SV1.time_dict[2] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.time_channel_VS1_SV1.time_dict[3] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.time_channel_VS1_SV1.time_dict[4] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.time_channel_VS1_SV1.time_dict[5] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.time_channel_VS1_SV1.time_dict[6] = [
                (dt.time(0, 0), True),
                (dt.time(3, 0), False),
                (dt.time(23, 0), True),
                (dt.time(14, 0), False),
                (dt.time(9, 0), True)
        ]
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()


    @asyncio.coroutine
    def async_5sec(self):
        while True:
            yield from asyncio.sleep(5)
            # 5seconds loop
            self.ActTimeLoop2 = time.time()
            # Run check if the sun warm pump should go
            # self.VS1_CP2_Class.Man = Control_of_CP2(
            # self.Weather_State,
            # self.VS1_GT3.temp,
            # self.SUN_GT2.temp,
            # self.SUN_GT1.temp)
            # Run control of sun warming pump
            # self.VS1_CP2_Class.main(0)
            # self.IOVariables['b_VS1_CP2_DO']['Value'] = (
                # self.VS1_CP2_Class.Out)

            '''Run check if the radiator pump should go,
                 if out temperature is under 10 degrees
            '''
            self.VS1_CP1_Class.Man = self.ThreeDayTemp < 10.0

            # Run control of sun warming pump
            self.VS1_CP1_Class.main(0)
            self.IOVariables['b_VS1_CP1_DO']['Value'] = (
                self.VS1_CP1_Class.Out)

            self.check_if_new_day()

            # Run modbus communication
            try:
                runModBus(self.IOVariables)
            except Exception as e:
                print('Something went wrong with the modbus!')


    @asyncio.coroutine
    def async_20sec(self):
        while True:
            yield from asyncio.sleep(20)
            # 20 seconds loop

            # Run the sensors
            try:
                self.VS1_GT1.RunMainTemp()
            except Exception as e:
                print('''
                        It went wrong time: {time} with {name}... {e}
                        ''').format(
                    time=dt.datetime.now(),
                    name=self.VS1_GT1.__class__,
                    e=e)
            try:
                self.VS1_GT2.RunMainTemp()
            except Exception as e:
                print('''
                        It went wrong time: {time} with {name}... {e}
                        ''').format(
                    time=dt.datetime.now(),
                    name=self.VS1_GT2.__class__,
                    e=e)
            try:
                self.VS1_GT3.RunMainTemp()
            except Exception as e:
                print('''
                        It went wrong time: {time} with {name}... {e}
                        ''').format(
                    time=dt.datetime.now(),
                    name=self.VS1_GT3.__class__,
                   e=e)
                # try:
                # self.SUN_GT1.RunMainTemp()
                # except Exception, e:
                # print('''
                # It went wrong time: {time} with {name}... {e}
                # ''').format(
                # time=dt.datetime.now(),
                # name=self.SUN_GT1.__class__,
                # e=e)
            try:
                self.SUN_GT2.RunMainTemp()
            except Exception as e:
                print("""
                        It went wrong time: {time} with {name}... {e}
                        """).format(
                    time=dt.datetime.now(),
                    name=self.SUN_GT2.__class__,
                    e=e)

            # Calculate setpoint
            self.Setpoint_VS1 = self.Komp.CountSP(self.VS1_GT3.temp)
            self.Setpoint_Log_VS1.value = self.Setpoint_VS1
            # print('SP {0:.1f}'.format(Setpoint_VS1))
            self.Setpoint_Log_VS1.main()

            # Run valve check
            self.VS1_SV1_Class.main(
                self.VS1_GT1.temp,
                self.Setpoint_VS1,
                self.IOVariables)

            # Run timechannel check, if True, change the setpoint
            self.VS1_SV1_SP_Down = self.time_channel_VS1_SV1.check_state()
            self.Komp.change_SP_lower(self.VS1_SV1_SP_Down)

    @asyncio.coroutine
    def async_1440sec(self):
        while True:
            self.Weather_State = GetData()
            yield from asyncio.sleep(1440)

    @asyncio.coroutine
    def async_3600sec(self):
        while True:
            yield from asyncio.sleep(3600)
            self.set_three_day_temp()

    def set_three_day_temp(self):
        self.ThreeDayTemp += self.VS1_GT3.temp / 72.0

    def show_values(self):
        print('GT1 {0:.1f}'.format(self.VS1_GT1.temp))
        print('GT2 {0:.1f}'.format(self.VS1_GT2.temp))
        print('GT3 {0:.1f}'.format(self.VS1_GT3.temp))
        # print('Solpanel - GT1 - uppe {0:.1f}'.format(self.SUN_GT1.temp))
        print('Solpanel - GT2 - nere {0:.1f}'.format(self.SUN_GT2.temp))
        print('SP {0:.1f}'.format(self.Setpoint_VS1))
        print('Nattsänkning {}'.format(self.VS1_SV1_SP_Down))
        print('Börvärde{}'.format(self.Komp.DictVarden))

    def check_if_new_day(self):
        if self.datumtid.day != dt.date.today().day:
            # if a new day...
            self.datumtid = dt.date.today()

    def data_func(self, read_or_write, data_request, write_value):
        print('using the func')
        # Method for communicating with asyncio socket server!
        self.shared_dict = {
            'self.Komp.DictVarden': self.Komp.DictVarden,
            self.VS1_CP1_Class.Name: {
                'Out': self.VS1_CP1_Class.Out,
                'Man': self.VS1_CP1_Class.Man,
                'S1': self.VS1_CP1_Class.S1,
                'S2': self.VS1_CP1_Class.S2,
                'S3': self.VS1_CP1_Class.S3,
                'T1': self.VS1_CP1_Class.T1,
                'T2': self.VS1_CP1_Class.T2,
                'T3': self.VS1_CP1_Class.T3,
                'LarmDelay': self.VS1_CP1_Class.LarmDelay
            },
            self.VS1_CP2_Class.Name: {
                'Out': self.VS1_CP2_Class.Out,
                'Man': self.VS1_CP2_Class.Man,
                'S1': self.VS1_CP2_Class.S1,
                'S2': self.VS1_CP2_Class.S2,
                'S3': self.VS1_CP2_Class.S3,
                'T1': self.VS1_CP2_Class.T1,
                'T2': self.VS1_CP2_Class.T2,
                'T3': self.VS1_CP2_Class.T3,
                'LarmDelay': self.VS1_CP2_Class.LarmDelay
            },
            self.VS1_SV1_Class.Name: {
                'deadband': self.VS1_SV1_Class.deadband,
                'Time_Open': self.VS1_SV1_Class.Time_Open,
                'Time_Close': self.VS1_SV1_Class.Time_Close,
                'Open_IO': self.VS1_SV1_Class.Open_IO,
                'Close_IO': self.VS1_SV1_Class.Close_IO
            },
            'self.VS1_GT1.temp': self.VS1_GT1.temp,
            'self.VS1_SV1_SP_Down': self.VS1_SV1_SP_Down,
            'self.VS1_GT2.temp': self.VS1_GT2.temp,
            'self.VS1_GT3.temp': self.VS1_GT3.temp,
            'self.SUN_GT2.temp': self.SUN_GT2.temp,
            'self.Setpoint_VS1': self.Setpoint_VS1,
            'time': time.time(),
            'IOVariables': self.IOVariables,
            'update_from_flask': False,
            'update_from_main': False,
            'self.Komp.value_to_lower': self.Komp.value_to_lower,
            'self.Weather_State': self.Weather_State
        }
        if read_or_write is 'r':
            return self.shared_dict[data_request]
        elif read_or_write is 'w':
            print('Changing value in main {}'.format(eval(data_request)))
            exec('{} = {}'.format(data_request, write_value))
            print('Changed value in main {}'.format(eval(data_request)))




def main():
    ML = MainLoop()
    # threading.Thread(target=ML.FlaskLoop).start()
    # threading.Thread(target=ML.control_loop).start()
    # threading.Thread(target=ML.interaction_loop).start()
    # threading.Thread(target=ML.interact).start()



if __name__ == '__main__':
    main()
