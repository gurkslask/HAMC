#! /usr/bin/python3

import socket
import json

main_menu_string = '''
Home-automation menu:
                1. Change Setpoint
                2. Show values
                3. Show weather
                4. Toggle test bit
                5. Change nightsink temperature
                0. Exit
'''
'''choices = {
    "1": change_sp,
    "2": show_values,
    "3": show_weather,
    "4": toggle_out,
    "5": change_nightsink,
    "0": exit
}'''


def show_values():
    message = {'r': ['VS1_GT1']}
    message = call_server(message)
    print(message)


def change_sp():
        value1 = input('Enter outside temperature: ')
        value2 = input('Enter forward temperature: ')
        try:
            actual_value = call_server({'r': ['self.Komp.DictVarden']})
            print(actual_value, type(actual_value))
            #actual_value = dict(actual_value)
            actual_value[str(value1)] = int(value2)
            call_server({'w': ['self.Komp.DictVarden', actual_value]})
        except SyntaxError as e:
            print('Invalid values entered, {}'.format(e))


choices = {
    "1": change_sp,
    "2": show_values,
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
        stop=True


# Echo client program
def call_server(message):
    message = json.dumps(message)
    HOST = '127.0.0.1'    # The remote host
    PORT = 5004              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message.encode())
    data = s.recv(1024)
    s.close()
    return json.loads(data.decode())
    # print 'Received', repr(data)

def data_handler(data):
    f_data = call_server(data)
    print('Här är lite data {}'.format(f_data))

if __name__ == '__main__':
    dialoge()
