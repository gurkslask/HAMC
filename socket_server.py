#!/usr/bin/python3

__author__ = 'alexander'

import asyncio

'''socketserver'''

host = 'localhost'
port = 5004
my_dict = {
    'Value1': 42.24
}


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

    def data_send(self, data):
        self.transport.write(data)
