from request import Request
from threading import Thread
import pagegen import generate_page
import response
import socket
import sys
import os
import re

default_port = 9000


def main():
    print('starting...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = default_port
    for i in range(10):
        try:
            sock.bind((socket.gethostname(), port))
            sock.listen(5)
            break
        except:
            port += 1

    ip = socket.gethostbyname(socket.gethostname())
    print('server started on', '{0}:{1}'.format(ip, port))

    while True:
        client_sock, client_addr = sock.accept()
        print('Connection from', client_addr, end='\n\n')
        t = Thread(target=handleRequest, args=(client_sock,))
        t.start()

def handleRequest(client_sock):
    raw_req = receive(client_sock)
    if raw_req:
        try:
            req = Request(raw_req)
            req.uri.root_with(root_dir)
            print(req, end='\n\n')
            response = req_type_to_func[req.method](req)
        except:
            response = response.Response(403)
        respond(client_sock, response)

def receive(client_sock):
    raw_req = client_sock.recv(2048)
    return raw_req

def respond(client_sock, data):
    client_sock.send(data)
    client_sock.shutdown(1)
    client_sock.close()

'''
---------------
REQUEST METHODS
---------------
'''

def get_request(req):
    resource = req.uri.resource
    page = generate_page(req.uri)
    if req.uri.prefix == 'p':
        resp = response.Response(201, page, resource)
    elif req.uri.prefix == 'r' or req-uri-prefix == 'd':
        resp = response.Response(200, page, resource)
    return resp.encode()

def post_request(req):
    print('POST with', req.uri)
    return

def head_request(req):
    return


root_dir = os.getcwd()
def find_server_path():
    server_dir = ''
    for a, b in zip(os.getcwd(), root_dir):
        if not a == b:
            server_dir += a
    return server_dir
server_dir = find_server_path()

req_type_to_func = {
    'GET' : get_request,
    'POST' : post_request,
    'HEAD' : head_request,
    'OPTIONS': option_request,
}

if __name__ == '__main__':
    main()
