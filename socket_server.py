#!/usr/bin/python3

import asyncio
import json

__author__ = 'alexander'

'''socketserver'''

host = 'localhost'
port = 5004
my_dict = {
    'Value1': '42.24'
}


class EchoServerClientProtocol(asyncio.Protocol):
    def __init__(self, hdata):
        # data_func method
        self.HAMC_data = hdata

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = json.loads(data.decode())
        # message = data.decode()
        print('Data received: {!r}, {}'.format(message, type(message)))
        for i in message:
            print(i)
            if i is 'w':
                pass
            elif i is 'r':
                for value_to_read in message[i]:
                    try:
                        data_to_send = str(json.dumps(self.HAMC_data('r', value_to_read, None))).encode()
                        print('Send: {!r}'.format(data_to_send))
                        self.transport.write(data_to_send)

                    except KeyError:
                        data_to_send = str(
                            json.dumps(
                                'KeyError: {}'.format(
                                    value_to_read
                                    )
                                )
                            ).encode()
                        print('Send: {!r}'.format(data_to_send))
                        self.transport.write(data_to_send)

        print('Close the client socket')
        self.transport.close()

    def data_send(self, data):
        self.transport.write(data)
