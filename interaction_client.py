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
    message = {'r': ['Weather_State']}
    message = call_server(message)
    print(message['Weather_State'])

def show_values():
    message = {'r': ['VS1_GT1',
                     'VS1_GT2',
                     'VS1_GT3',
                     'SUN_GT2',
                     'Setpoint_VS1',
                     'VS1_SV1_SP_Down',
                     'Komp',
                     'ThreeDayTemp'
    ]}
    message = call_server(message)
    print('GT1 {0:.1f}'.format(message['VS1_GT1']['PV']))
    print('GT2 {0:.1f}'.format(message['VS1_GT2']['PV']))
    print('GT3 {0:.1f}'.format(message['VS1_GT3']['PV']))
    # print('Solpanel - GT1 - uppe {0:.1f}'.format(SUN_GT1))
    print('Solpanel - GT2 - nere {0:.1f}'.format(message['SUN_GT2']['PV']))
    print('SP {0:.1f}'.format(message['Setpoint_VS1']['SP']))
    print('Nattsänkning {}'.format(message['VS1_SV1_SP_Down']))
    print('Börvärde{}'.format(message['Komp']['DictVarden']))
    print('Tredagarstemp: {}'.format(message['ThreeDayTemp']))


def change_sp():
        value1 = input('Enter outside temperature: ')
        value2 = input('Enter forward temperature: ')
        try:
            request_string = 'Komp.DictVarden'
            actual_value = call_server({'r': ['Komp']})
            print(actual_value, type(actual_value))
            print(actual_value['Komp']['DictVarden'])
            #actual_value = dict(actual_value)
            actual_value['Komp']['DictVarden'][int(value1)] = int(value2)
            print(actual_value, type(actual_value))
            call_server({'w': [['self.Komp.DictVarden', actual_value['Komp']['DictVarden']]]})


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
