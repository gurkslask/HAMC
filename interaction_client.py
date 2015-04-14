#! /usr/bin/python3

import pickle
from connect_to_socket import call_server

main_menu_string = '''
Home-automation menu:
                1. Change Setpoint
                2. Show values
                3. Show weather
                5. Change nightsink temperature
                0. Exit
'''

def change_nightsink():
    try:
        nightsink = float(input('Enter nightsink temperature: '))
    except ValueError as e:
        print('Value {} is not a float'.format(nightsink))
    finally:
        call_server({'w': [['self.Komp.value_to_lower', nightsink]]})

def show_weather():
    message = {'r': ['self.Weather_State']}
    message = call_server(message)
    print(message)

def show_values():
    message = {'r': ['self.VS1_GT1.temp',
                     'self.VS1_GT2.temp',
                     'self.VS1_GT3.temp',
                     'self.SUN_GT2.temp',
                     'self.Setpoint_VS1',
                     'self.VS1_SV1_SP_Down',
                     'self.Komp.DictVarden',
                     'self.ThreeDayTemp'
    ]}
    message = call_server(message)
    print('GT1 {0:.1f}'.format(message['self.VS1_GT1.temp']))
    print('GT2 {0:.1f}'.format(message['self.VS1_GT2.temp']))
    print('GT3 {0:.1f}'.format(message['self.VS1_GT3.temp']))
    # print('Solpanel - GT1 - uppe {0:.1f}'.format(self.SUN_GT1.temp))
    print('Solpanel - GT2 - nere {0:.1f}'.format(message['self.SUN_GT2.temp']))
    print('SP {0:.1f}'.format(message['self.Setpoint_VS1']))
    print('Nattsänkning {}'.format(message['self.VS1_SV1_SP_Down']))
    print('Börvärde{}'.format(message['self.Komp.DictVarden']))
    print('Tredagarstemp: {}'.format(message['self.ThreeDayTemp']))


def change_sp():
        value1 = input('Enter outside temperature: ')
        value2 = input('Enter forward temperature: ')
        try:
            request_string = 'self.Komp.DictVarden'
            actual_value = call_server({'r': [request_string]})[request_string]
            print(actual_value, type(actual_value))
            #actual_value = dict(actual_value)
            actual_value[int(value1)] = int(value2)
            print(actual_value, type(actual_value))
            call_server({'w':
                [
                    [
                        'self.Komp.DictVarden', actual_value
                    ]
                ]
            })


        except SyntaxError as e:
            print('Invalid values entered, {}'.format(e))

choices = {
    "1": change_sp,
    "2": show_values,
    "3": show_weather,
    "5": change_nightsink,
    "0": exit
}


def dialoge():
    stop = False
    while not stop:
        print(main_menu_string)
        choice = input('Enter number of choice:')
        try:
            int(choice)
            action = choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))
        except SyntaxError:
            print('Choice must be a integer')
            pass
        # stop=True



if __name__ == '__main__':
    dialoge()
