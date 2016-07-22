#!Users/Min/anaconda3/bin/python

from threading import Thread
from sys import argv
import os
import time
import socket
import re
import response


def handleRequest(sock):
    status_code = 200
    request = sock.recv(2048).decode()
    if request:
        params = parse(request)
        path = params['path']
        resource = params['resource']
        print('path:', path)
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
    path = os.path.join(_root, resource)
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

    with open('./temps/dir_template.html') as dir_template:
        html = dir_template.read()

    subdirs = os.listdir(path)
    with open('./temps/table_row.html') as row_template:
        template = row_template.read()

    table_rows = []
    for subdir in subdirs:
        fullpath = os.path.join(directory, subdir)
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fullpath)
        link = template.replace('MTIME', time.ctime(mtime))
        link = link.replace('SIZE', str(size))
        link = link.replace('ITEM', subdir)
        link = link.replace('PATH', os.path.join(fullpath))
        table_rows.append(link)
    links = '\n'.join(table_rows)

    directory = 'Root' if not directory else directory

    html = html.replace('<!--ITEMS-->', links)
    html = html.replace('<!--DIRECTORY-->', directory)
    html = html.replace('<!--TITLE-->', 'Yaolink')

    return html

if __name__ == '__main__':
    port = 9000
    if len(argv) > 1:
        port = int(argv[1])

    _root = os.getcwd()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(10):
        try:
            s.bind((socket.gethostname(), port))
            s.listen(5)
            break
        except:
            port += 1

    ip = '{0}:{1}'.format(socket.gethostbyname(socket.gethostname()), port)
    print('server started on', ip)

    while True:
        clientSock, clientAddr = s.accept()
        t = Thread(target=handleRequest, args=(clientSock,))
        t.start()
