__author__ = 'alexander'

import json
import socket
import sys
import tempfile

# Echo client program


def call_server(message):
    f = tempfile.NamedTemporaryFile(mode='w+')
    HOST = '127.0.0.1'    # The remote host
    PORT = 5004              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    json.dump(message, f)
    jdata = json.dumps(message)
    # print(open(f.name, 'r').read())
    s.sendall(jdata.encode('utf-8'))
    data = s.recv(1024)
    s.close()
    return json.loads(data.decode('utf-8'))
    # print 'Received', repr(data)

if __name__ == '__main__':
    command_str = sys.argv[1].replace('\n', '').split(':')
    print(command_str)
    if len(command_str) == 2: #if read
        command = {command_str[0]: [command_str[1]]}
    elif len(command_str) == 3: #if write
        command = {command_str[0]: [[command_str[1], command_str[2]]]}

    print(call_server(command))
