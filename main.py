#!/usr/bin/python
# -*- coding: utf-8 -*-
from ds1820class import DS1820
from ds1820class import Write_temp
from Kompensering import Kompensering
from OpenCloseValveClass import OpenCloseValve
from IOdef import IOdef
from scraping import GetData
from PumpControl import PumpControl, Control_of_CP2
from ModBus import runModBus
import time
import threading
import pickle
import datetime
import datetime as dt


class MainLoop():
    def __init__(self):

        #Declare IO Variables
        self.IOVariables = IOdef()

        #Declare temperaturecompensation
        self.Komp = Kompensering()
        self.Komp.SetVarden(20, 17)
        self.Komp.SetVarden(-10, 40)
        self.Komp.SetVarden(0, 35)
        self.Komp.SetVarden(10, 30)
        self.Komp.SetVarden(-20, 65)
        self.Komp.SetMax(65)
        self.Komp.SetMin(20)

        #Loggin of the compensation
        self.Setpoint_VS1 = 0.0
        self.Setpoint_Log_VS1 = Write_temp(self.Setpoint_VS1, 'VS1_Setpoint')

        #Declare temperature sensors
        #Framledning
        self.VS1_GT1 = DS1820('28-00000523a1cb')
        self.VS1_GT1.Comment = '''
        This is the sensor that measures
        the water temperature to the radiators'''
        self.VS1_GT1.Name = 'VS1_GT1'
        #Retur
        self.VS1_GT2 = DS1820('28-00000524056e')
        self.VS1_GT2.Comment = '''This is the sensor that measures
         the water temperature from the radiators'''
        self.VS1_GT2.Name = 'VS1_GT2'
        #Ute
        self.VS1_GT3 = DS1820('28-0000052407e0')
        self.VS1_GT3.Comment = '''This is the sensor that measures
         the outdoor temperature'''
        self.VS1_GT3.Name = 'VS1_GT3'
        #@Solar panels
        #self.SUN_GT1 = DS1820('28-00000523ab8e')
        #self.SUN_GT1.Comment = '''This is the sensor that measures
        #the water temperature to the solar panels'''
        #self.SUN_GT1.Name = 'SUN_GT1'
        # After solar panels
        self.SUN_GT2 = DS1820('28-0000052361be')
        self.SUN_GT2.Comment = '''This is the sensor that measures
         the water temperature from the solar panels'''
        self.SUN_GT2.Name = 'VS1_GT2'

        #Declare logging interval
        self.VS1_GT1.SetWriteInterval(60)
        self.VS1_GT2.SetWriteInterval(60)
        self.VS1_GT3.SetWriteInterval(60)
        #self.SUN_GT1.SetWriteInterval(60)
        self.SUN_GT2.SetWriteInterval(60)

        #Declare Heating valve
        self.VS1_SV1_Class = OpenCloseValve()
        self.VS1_SV1_Class.Name = 'VS1_SV1'
        self.VS1_SV1_Class.Open_IO = 'b_VS1_SV1_OPEN_DO'
        self.VS1_SV1_Class.Close_IO = 'b_VS1_SV1_CLOSE_DO'

        #Initialize the loops
        self.ActTimeLoop1 = time.time()
        self.ActTimeLoop2 = time.time()
        self.ActTimeLoop3 = time.time() - 14400
        self.ActTimeLoop4 = time.time()
        self.ActTimeLoop5 = time.time()

        #Declare Cirkulation pump sun heaters
        self.VS1_CP2_Class = PumpControl('SUN_P1')
        self.VS1_CP2_Class.Comment = '''This is the pump that pumps
         water up to the sun heaters'''
        #self.VS1_CP2_Class.Name='SUN_P1'

        #Declare Circualation pump for radiators in the house
        self.VS1_CP1_Class = PumpControl('VS1_CP1')
        self.VS1_CP1_Class.Comment = ('''This is the pump that supplies
         the heating radiators with hot water''')

        #Interaction menu
        self.choices = {
            "1": self.ChangeSP,
            "2": self.ShowValues,
            "3": self.ShowWeather,
            "4": self.ToggleOut,
            "0": self.exit
            }
        #Declare variebles
        self.Weather_State = ''
        self.exit_flag = False
        self.datumtid = datetime.date.today()
        self.ThreeDayTemp = 9.0

        #Declare Flask shared dictionary
        self.shared_dict = {
            'komp': self.Komp.DictVarden,
            self.VS1_CP1_Class.Name: self.VS1_CP1_Class.__dict__,
            self.VS1_CP2_Class.Name: self.VS1_CP2_Class.__dict__,
            self.VS1_SV1_Class.Name: self.VS1_SV1_Class.__dict__,
            self.VS1_GT1.Name: self.VS1_GT1.__dict__,
            self.VS1_GT2.Name: self.VS1_GT2.__dict__,
            self.VS1_GT3.Name: self.VS1_GT3.__dict__,
            self.SUN_GT2.Name: self.SUN_GT2.__dict__,
            'VS1_Setpoint': self.Setpoint_VS1,
            'IOVariables': self.IOVariables
            }
        self.choice = False

    def ControlLoop(self):
            while not self.exit_flag:
                '''This is the main loop'''
                if self.ActTimeLoop1 + 20 < time.time():
                    #20 seconds loop
                    #Reset time for next loop
                    self.ActTimeLoop1 = time.time()

                    #print('GT1 {0:.1f}'.format(GT1.RunMainTemp()))
                    #print('GT2 {0:.1f}'.format(VS1_GT2.RunMainTemp()))
                    #print('GT3 {0:.1f}'.format(VS1_GT3.RunMainTemp()))

                    #Run the sensors
                    try:
                        self.VS1_GT1.RunMainTemp()
                    except Exception, e:
                        print('''
                            It went wrong time: {time} with {name}... {e}
                            ''').format(
                            time=dt.datetime.now(),
                            name=self.VS1_GT1.__class__,
                            e=e)
                    try:
                        self.VS1_GT2.RunMainTemp()
                    except Exception, e:
                        print('''
                            It went wrong time: {time} with {name}... {e}
                            ''').format(
                            time=dt.datetime.now(),
                            name=self.VS1_GT2.__class__,
                            e=e)
                    try:
                        self.VS1_GT3.RunMainTemp()
                    except Exception, e:
                        print('''
                            It went wrong time: {time} with {name}... {e}
                            ''').format(
                            time=dt.datetime.now(),
                            name=self.VS1_GT3.__class__,
                            e=e)
                    #try:
                        #self.SUN_GT1.RunMainTemp()
                    #except Exception, e:
                        #print('''
                            #It went wrong time: {time} with {name}... {e}
                            #''').format(
                            #time=dt.datetime.now(),
                            #name=self.SUN_GT1.__class__,
                            #e=e)
                    try:
                        self.SUN_GT2.RunMainTemp()
                    except Exception, e:
                        print('''
                            It went wrong time: {time} with {name}... {e}
                            ''').format(
                            time=dt.datetime.now(),
                            name=self.SUN_GT2.__class__,
                            e=e)

                    #Calculate setpoint
                    self.Setpoint_VS1 = self.Komp.CountSP(self.VS1_GT3.temp)
                    self.Setpoint_Log_VS1.value = self.Setpoint_VS1
                    #print('SP {0:.1f}'.format(Setpoint_VS1))
                    self.Setpoint_Log_VS1.main()

                    #Run valve check
                    self.VS1_SV1_Class.main(
                        self.VS1_GT1.temp,
                        self.Setpoint_VS1,
                        self.IOVariables)
                    #Run logging of the state of the valve
                    #Run control of the valve

                    #Run modbus communication
                    try:
                        runModBus(self.IOVariables)
                    except Exception, e:
                        raise e
                        print('Something went wrong with the modbus!')

                if self.ActTimeLoop2 + 5 < time.time():
                    #5seconds loop
                    self.ActTimeLoop2 = time.time()
                    #Run check if the sun warm pump should go
                    #self.VS1_CP2_Class.Man = Control_of_CP2(
                        #self.Weather_State,
                        #self.VS1_GT3.temp,
                        #self.SUN_GT2.temp,
                        #self.SUN_GT1.temp)
                    #Run control of sun warming pump
                    self.VS1_CP2_Class.main(0)
                    self.IOVariables['b_VS1_CP2_DO']['Value'] = (
                        self.VS1_CP2_Class.Out)

                    '''Run check if the radiator pump should go,
                     if out temperature is under 10 degrees
                    '''
                    self.VS1_CP1_Class.Man = self.ThreeDayTemp < 10.0

                    #Run control of sun warming pump
                    self.VS1_CP1_Class.main(0)
                    self.IOVariables['b_VS1_CP1_DO']['Value'] = (
                        self.VS1_CP1_Class.Out)

                    self.CheckIfNewDay()

                    self.choice = not self.choice
                    self.InteractWithFlask(self.choice)

                    #print('Loop 2')

                if self.ActTimeLoop3 + 14400 < time.time():
                    #4 hour loop
                    self.ActTimeLoop3 = time.time()

                    self.Weather_State = GetData()


                if self.ActTimeLoop5 + 3600 < time.time():
                    '''Run Loop once a hour
                    '''
                    self.SetThreeDayTemp()


                time.sleep(1)

    def InteractionLoop(self):
        while not self.exit_flag:

            print("""Home-automation menu:
                1. Change Setpoint
                2. Show values
                3. Show weather
                4. Toggle test bit
                0. Exit
                """)
            choice = raw_input('Enter an option: ')
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

            #print('Fran klassen: Open - ' + str(self.VS1_SV1_Class.Man_Open_OUT))
            #print('Fran klassen: Close - ' + str(self.VS1_SV1_Class.Man_Close_OUT))
            #print('Fran databasen: Open - ' + str(self.IOVariables['b_SV_OPEN_DO']['Value']))
            #print('Fran databasen: Close - ' + str(self.IOVariables['b_SV_CLOSE_DO']['Value']))
            time.sleep(5)

    def SetThreeDayTemp(self):
        self.ThreeDayTemp = self.ThreeDayTemp + (self.VS1_GT3.temp / 72.0)

    def ChangeSP(self):
        value1 = input('Enter outside temperature: ')
        value2 = input('Enter forward temperature: ')
        try:
            self.Komp.DictVarden[int(value1)] = int(value2)
        except:
            print('Invalid values entered')

    def ShowValues(self):
        print('GT1 {0:.1f}'.format(self.VS1_GT1.temp))
        print('GT2 {0:.1f}'.format(self.VS1_GT2.temp))
        print('GT3 {0:.1f}'.format(self.VS1_GT3.temp))
        #print('Solpanel - GT1 - uppe {0:.1f}'.format(self.SUN_GT1.temp))
        print('Solpanel - GT2 - nere {0:.1f}'.format(self.SUN_GT2.temp))
        print('SP {0:.1f}'.format(self.Setpoint_VS1))

    def ShowWeather(self):
        print(self.Weather_State)

    def ToggleOut(self):
        self.IOVariables['b_Test']['Value'] = not self.IOVariables['b_Test']['Value']
        print('b_test info: {testvar}'.format(testvar=self.IOVariables['b_Test']))

    def exit(self):
        print('System exits...')
        #shutdown_server()
        print('System exits...')
        self.exit_flag = True
        print('System exits...')
        time.sleep(5)
        raise SystemExit

    def CheckIfNewDay(self):
        if self.datumtid.day != datetime.date.today().day:
            #if a new day...
            self.datumtid = datetime.date.today()

    def InteractWithFlask(self, choice):
        '''Dump shared_dict to a pickle, or load it'''
        if choice:
            with open('shared_dict', 'wb+') as f:
                pickle.dump(self.shared_dict, f)
        elif not choice:
            with open('shared_dict', 'rb') as f:
                self.shared_dict.update(pickle.load(f))


def main():
    ML = MainLoop()
    #threading.Thread(target=ML.FlaskLoop).start()
    threading.Thread(target=ML.ControlLoop).start()
    threading.Thread(target=ML.InteractionLoop).start()


if __name__ == '__main__':
    main()
