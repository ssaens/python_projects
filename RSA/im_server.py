from threading import Thread
from sys import argv
import socket

host = '192.168.0.101'
port = int(argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

def listen(f, t):
    while True:
        data = f.recv(1024)
        if not data:
            f.close()
        t.send(data)

def waitForName(q):
    while True:
        name = q.recv(1024)
        if name:
            return name

s.listen(2)
print('listening...')
q1, addr1 = s.accept()
print('connection 1 established')
print('listening...')
q2, addr2 = s.accept()
print('connection 2 established')

q1.send('linked'.encode('UTF-8'))
name1 = waitForName(q1)
q2.send('linked'.encode('UTF-8'))
name2 = waitForName(q2)
q2.send(name1)
q1.send(name2)

user1 = Thread(target=listen, args=(q1, q2))
user2 = Thread(target=listen, args=(q2, q1))

user1.start()
user2.start()
