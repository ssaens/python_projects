from threading import Thread
from sys import argv
from os import *
import socket
import re

__root = '/Users/Min/projects/python_projects'

def handleRequest(sock):
    try:
        request = sock.recv(2048).decode()
        params = parse(request)
        requested = params['resource']
        response = ''
        if path.exists(requested):
            if path.isfile(requested):
                with open(requested) as fh:
                    response = ''.join(fh.readlines())
            elif path.isdir(requested):
                response = requested
        else:
            response = 'error: path not found'

        sock.send(response.encode())
        sock.shutdown(1)
        sock.close()
    except Exception as e:
        print('Error in handleRequest: ' + str(e))
        sock.close()

def parse(request):
    attributes = request.split('\n')
    method, resource, version = attributes[0].split()
    resource = path.join(__root, resource[1:])
    params =    {'method' : method.strip(),
                'resource' : resource.strip(),
                'version' : version.strip(),
                }

    for i in range(1, len(attributes)):
        line = attributes[i]
        match = re.match('(.*):(.*)', line)
        if match:
            params[match.group(1)] = match.group(2)

    print(params)
    return params

def startServer():
    port = int(argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(5)
    print('listening')

    while True:
        clientSock, clientAddr = s.accept()
        t = Thread(target=handleRequest, args=(clientSock,))
        t.start()

if __name__ == '__main__':
    startServer()
