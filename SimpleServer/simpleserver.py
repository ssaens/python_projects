from threading import Thread
from sys import argv
import os
import time
import socket
import re
import response

__root = '.'

def handleRequest(sock):
    status_code = 200
    request = sock.recv(2048).decode()
    request += sock.recv(2048).decode()
    request += sock.recv(2048).decode()
    if request:
        params = parse(request)
        path = params['path']
        resource = params['resource']
        print('path: ' + path)
        print('resource: %s\n'%resource)

        content = ''
        if resource and resource[0] == '.':
            status_code = 403
            content = '403 Denied'
        elif os.path.exists(path):
            if os.path.isfile(path):
                with open(path, 'rb') as fh:
                    content = fh.read()
            elif os.path.isdir(path):
                status_code = 201
                content = generate_dir_html(path, resource).encode()
                resource = 'dir'
        else:
            status_code = 404
            content = '404 File Not Found'.encode()

        r = response.Response(status_code, content, resource)

        sock.send(r.encode())
        sock.shutdown(1)
    sock.close()

def parse(request):
    print(request)
    attributes = request.split('\n')
    method, resource, version = attributes[0].split()
    while resource.startswith('/'):
        resource = resource[1:]
    path = os.path.join(__root, resource)
    params =    {'method' : method.strip(),
                'path' : path.strip(),
                'resource' : resource.strip(),
                'version' : version.strip(),
                }

    for i in range(1, len(attributes)):
        line = attributes[i]
        match = re.match('(.*?):(.*)', line)
        if match:
            params[match.group(1)] = match.group(2)

    return params

def generate_dir_html(path, directory):
    if directory.endswith('/'):
        directory = directory[:-1]
    subdirs = os.listdir(path)
    html = '<HTML><head><title>{0}</title></head><body><h2>{0}</h2><ul>'.format(directory)
    for subdir in subdirs:
        if directory:
            link = '/{0}/{1}'.format(directory, subdir)
        else:
            link = '{0}/{1}'.format(directory, subdir)
        html += '<li><a href=\"{0}\">{1}</a></li>'.format(link, subdir)
    html += '</ul></body></HTML>'
    return html

if __name__ == '__main__':
    port = int(argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(5)
    print('server started on {0}:{1}'.format(socket.gethostbyname(socket.gethostname()), port))

    while True:
        clientSock, clientAddr = s.accept()
        t = Thread(target=handleRequest, args=(clientSock,))
        t.start()
