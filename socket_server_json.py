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
        message = json.loads(data.decode('utf-8'))
        for read_or_write in message:
            if read_or_write is 'w':
                for value_to_write in message[read_or_write]:
                    #value_to_write = value_to_write.split(',')
                    self.HAMC_data('w', value_to_write[0], value_to_write[1])
            elif read_or_write is 'r':
                data_to_send = {}
                for value_to_read in message[read_or_write]:
                    try:
                        data_to_send[value_to_read] = self.HAMC_data('r', value_to_read, None)
                    except KeyError:
                        data_to_send[value_to_read] = 'Keyerror'
                self.transport.write(json.dumps(data_to_send).encode('utf-8'))

        print('Close the client socket')
        self.transport.close()

    def data_send(self, data):
        self.transport.write(data)

