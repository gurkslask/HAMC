#! /usr/bin/python3

import asyncio
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


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event lop')
        self.loop.stop()


def interact():
    while True:
        print('Whaddayawant?!')
        choice = input('Yo?!')
        if choice is 'w':
            call_server(json.dumps({
                'r':
                    [
                        'komp',
                        'VS1_Setpoint',
                        'Komp.DictVarden'
                    ],
                'w':
                    []
                }
                ))
        if choice is 's':
            call_server(json.dumps({
                'r':
                    [
                        'komp',
                        'VS1_Setpoint',
                        'Komp.DictVarden'
                    ],
                'w':
                    [
                        'VS1_Setpoint, 42'
                    ]
                }
                ))


def call_server(message):
    loop = asyncio.get_event_loop()
    # message = 'Hello World!'
    coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                                  '127.0.0.1', 5004)
    loop.run_until_complete(coro)
    loop.run_forever()
    # loop.close()


if __name__ == '__main__':
    interact()
