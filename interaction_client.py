#! /usr/bin/python3

import socket
import pickle

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
    message = {'r': ['VS1_GT1', 'VS1_GT2']}
    message = call_server(message)
    print(message)


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


# Echo client program
def call_server(message):
    message = pickle.dumps(message)
    HOST = '127.0.0.1'    # The remote host
    PORT = 5004              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    return pickle.loads(data)
    # print 'Received', repr(data)

if __name__ == '__main__':
    dialoge()
