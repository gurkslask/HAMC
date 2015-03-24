#!/usr/bin/python3

import asyncio
import json

__author__ = 'alexander'

'''socketserver'''


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
        print('Data received: {!r}, {}'.format(message, type(message)))
        for read_or_write in message:
            if read_or_write is 'w':
                for value_to_write in message[read_or_write]:
                    value_to_write = value_to_write.split(',')
                    print('Before: {}'.format(
                        self.HAMC_data(
                            'r', value_to_write[0], None
                            )
                        )
                    )
                    self.HAMC_data('w', value_to_write[0], value_to_write[1])
                    print('After: {}'.format(
                        self.HAMC_data(
                            'r', value_to_write[0], None
                            )
                        )
                    )
            elif read_or_write is 'r':
                for value_to_read in message[read_or_write]:
                    try:
                        data_to_send = str(
                            json.dumps(
                                self.HAMC_data(
                                    'r',
                                    value_to_read,
                                    None
                                    )
                                )
                            ).encode()
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


class EchoServerClientProtocol3(asyncio.Protocol):
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
        print('Close the client socket')
        self.transport.close()

    def data_send(self, data):
        self.transport.write(data)
