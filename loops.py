__author__ = 'alexander'

import asyncio

def seconds5(self):
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
    self.VS1_CP2_Class.main(0)
    self.IOVariables['b_VS1_CP2_DO']['Value'] = (
        self.VS1_CP2_Class.Out)

    '''Run check if the radiator pump should go,
         if out temperature is under 10 degrees
        '''
    self.VS1_CP1_Class.Man = self.ThreeDayTemp < 10.0

    # Run control of sun warming pump
    self.VS1_CP1_Class.main(0)
    self.IOVariables['b_VS1_CP1_DO']['Value'] = (
        self.VS1_CP1_Class.Out)

    self.check_if_new_day()

    # self.choice = not self.choice
    # self.interact_with_flask(self.choice)

    # print('Loop 2')


    # Run modbus communication
    try:
        runModBus(self.IOVariables)
    except Exception as e:
        print('Something went wrong with the modbus!')
        raise e
    return self

def seconds20(self):
    yield from asyncio.sleep(20)
    # 20 seconds loop
    # Reset time for next loop
    self.ActTimeLoop1 = time.time()

    # print('GT1 {0:.1f}'.format(GT1.RunMainTemp()))
    # print('GT2 {0:.1f}'.format(VS1_GT2.RunMainTemp()))
    # print('GT3 {0:.1f}'.format(VS1_GT3.RunMainTemp()))

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
        print('''
                It went wrong time: {time} with {name}... {e}
                ''').format(
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
    return self


def seconds1440():
    self.Weather_State = GetData()
    yield from asyncio.sleep(1440)

def seconds3600():
    yield from asyncio.sleep(3600)