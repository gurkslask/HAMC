#! /usr/bin/python3

import asyncio
import json

glob_var = None

main_menu_string = '''
Home-automation menu:
                1. Change Setpoint
                2. Show values
                3. Show weather
                4. Toggle test bit
                5. Change nightsink temperature
                0. Exit
'''


def change_sp():
        value1 = input('Enter outside temperature: ')
        value2 = input('Enter forward temperature: ')
        try:
            actual_value = interact_with_main({'r': ['self.Komp.DictVarden']})
            print(actual_value)
            actual_value[int(value1)] = int(value2)
            interact_with_main({'w': ['self.Komp.DictVarden', actual_value]})
        except ValueError as e:
            print('Invalid values entered, {}'.format(e))

'''choices = {
    "1": change_sp,
    "2": show_values,
    "3": show_weather,
    "4": toggle_out,
    "5": change_nightsink,
    "0": exit
}'''
choices = {
    "1": change_sp,
    "0": exit
}


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        self.decoded_data = data.decode()
        print('Data received: {!r}'.format(data.decode()))
        glob_var = self.decoded_data
        print(glob_var)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


def dialoge():
    while True:
            print(main_menu_string)
            choice = input('Enter number of choice:')
            try:
                int(choice)
                action = choices.get(choice)
                if action:
                    action()
                else:
                    print("{0} is not a valid choice".format(choice))
            except ValueError:
                print('Choice must be a integer')
                pass


def interact_with_main(variable_list):
    return call_server(json.dumps(variable_list))


def conn(message, loop):
    # protocol_object =  EchoClientProtocol(message,loop)
    return lambda: EchoClientProtocol(message, loop)


def call_server(message):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(conn(message, loop),
                                  '127.0.0.1', 5004)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    dialoge()
