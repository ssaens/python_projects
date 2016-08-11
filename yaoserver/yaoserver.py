from communications import Request, Response
from threading import Thread
from time import gmtime, strftime
from dbconnect import TableInserter
import socket
import sys
import re
import os

port = None
app_root = None

def init():
    sys.path.append(__file__)

    settings = dict()
    with open('server.conf') as conf:
        for line in conf:
            setting = re.match('(.*?) : (.*)', line)
            if setting:
                settings[setting.group(1)] = setting.group(2)

    global port, server_root, app_root
    port = int(settings['PORT'])
    app_root = settings['APPLICATION_ROOT']
    if os.path.isdir(app_root):
        sys.path.append(app_root)
    else:
        raise Exception('Invalid Application Root')

    try:
        global connection_logger, req_logger, res_logger
        connection_logger = TableInserter()
        req_logger = TableInserter()
        res_logger = TableInserter()
    except Exception as e:
        print('Warning: MySQL Inserter Failed to instantiate')
        print(str(e))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = socket.gethostbyname(socket.gethostname())
    sock.bind((socket.gethostname(), port))
    sock.listen(5)
    print('server started on {0}:{1}\n\n'.format(ip, port))
    connection = 0

    while True:
        client_sock, client_addr = sock.accept()
        print(connection, ': Connection from', client_addr)
        connection += 1
        t = Thread(target=handle_request, args=(client_sock, client_addr))
        t.start()

def handle_request(client, addr):
    raw_req = receive(client)
    res = Response()
    creation_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    res.add_header('Date', creation_time)
    connection_open = True

    try:
        req = Request(raw_req)
        print(req)
        if 'Connection' in req.headers:
            if req.headers['Connection'] == 'keep-alive':
                res.add_header('Connection', 'keep-alive')
        match_uri(req.uri, req, res)
        log(addr, req, res)
    except Exception as e:
        print(str(e) + '\n')
        res.clear()
        if str(e) == 'Empty Request String':
            connection_open = False
            res.set_code(400)
        else:
            res.set_code(500)

    if connection_open:
        respond(client, res)


def receive(client):
    raw = client.recv(2048)
    return raw

def respond(client, res):
    print(res)
    client.send(res.encode())
    client.shutdown(1)
    client.close()

def match_uri(uri, req, res):
    matched = False
    for pattern in switchboard.uri_patterns:
        if pattern(uri, req, res):
            matched = True
            break
    if not matched:
        print('No match found')
        res.set_code(404)

def log(addr, req, res):
    print(addr)
    print(req)
    print(res)


if __name__ == '__main__':
    print('yaoserver v0.2.0')
    init()
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    try:
        import switchboard
    except Exception as e:
        print('Missing switchboard.py in application module')
        raise e
    main()
