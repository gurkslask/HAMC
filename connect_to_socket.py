__author__ = 'alexander'

import pickle
import socket
import sys

# Echo client program


def call_server(message):
    message = pickle.dumps(message)
    HOST = '192.168.1.138'    # The remote host
    PORT = 5008              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    return pickle.loads(data)
    # print 'Received', repr(data)

if __name__ == '__main__':
    command_str = sys.argv[1].replace('\n', '').split(':')
    if len(command_str) == 2: #if read
        command = {command_str[0]: [command_str[1]]}
    elif len(command_str) == 3: #if write
        command = {command_str[0]: [[command_str[1], command_str[2]]]}

    print(call_server(command))
