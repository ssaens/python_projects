from request import Request
from threading import Thread
from pagegen import generate_page
import response
import socket
import sys
import os
import re

root_dir = os.getcwd()
default_port = 9000
req_type_to_func = None

def main():
    global req_type_to_func

    server_dir = os.getcwd()
    req_type_to_func = {
        'GET' : get_request,
        'POST' : post_request,
        'HEAD' : head_request,
    }

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
    req = Request(raw_req)
    to_send = req_type_to_func[req.method](req)
    respond(client_sock, to_send)

def receive(client_sock):
    raw_req = client_sock.recv(2048)
    return raw_req

def respond(client_sock, data):
    client_sock.send(data)
    client_sock.shutdown(1)
    client_sock.close()

def get_request(req):
    resource = req.uri
    print('GET request for', resource)
    while resource.startswith('/'):
        resource = resource[1:]
    fullpath = os.path.join(root_dir, resource)
    resp = response.Response(201, generate_page(fullpath, resource), resource)
    return resp.encode()

def post_request(req):
    print('POST with', req.uri)
    return

def head_request(req):
    return

if __name__ == '__main__':
    main()
