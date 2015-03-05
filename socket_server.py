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
        message = data.decode()
        print('Data received: {!r}, {}'.format(message, type(message)))

        if message == 'hej':
            # data_to_send = my_dict['Value1']
            # data_to_send = str(json.dumps(my_dict['Value1'])).encode()
            data_to_send = str(json.dumps(self.HAMC_data)).encode()
            print('Send: {!r}'.format(data_to_send))
            self.transport.write(data_to_send)
        else:
            print('Send: {!r}'.format(message))
            self.transport.write(data)
        print('Close the client socket')
        self.transport.close()

    def data_send(self, data):
        self.transport.write(data)
