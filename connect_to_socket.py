__author__ = 'alexander'

import pickle
import socket
import sys

# Echo client program
def call_server(message):
    message = pickle.dumps(message)
    HOST = '127.0.0.1'    # The remote host
    PORT = 5004              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    return pickle.loads(data)
    # print 'Received', repr(data)

if __name__ == '__main__':
    command = sys.argv[1].replace('\n', ''), split(':')
    print(call_server({command[0], command[1]}))