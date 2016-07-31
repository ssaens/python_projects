from communications import Request, Response
from threading import Thread
import socket

def main():
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
        t = Thread(target=handle_request, args=(client_sock,))
        t.start()

def handle_request(client):
    raw_req = receive(client)
    res = Response()
    try:
        req = Request(raw_req)
        req_method = req_type_to_func[req.method]
        req_method(req, res)
    except Exception as e:
        print(str(e))
        response.set_code(400)
    respond(client, res)

def receive(client):
    raw = client.recv(2048)
    return raw

def respond(client, msg):
    client.send(msg)
    client.shutdown(1)
    client.close()

''' REQUEST METHODS '''

def get_request(req, res):

def post_request(req, res):

def head_requst(req, res):

def option_request(req, res):


req_type_to_func = {
    'GET' : get_request,
    'POST' : post_request,
    'HEAD' : head_request,
    'OPTIONS': option_request,
}

supported_tokens = {'p', 'd', 'r'}

if __name__ == '__main__':
    main()
