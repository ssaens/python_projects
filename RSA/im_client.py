import socket
from threading import Thread
from time import sleep
from sys import argv

host='192.168.0.101'
port = int(argv[1])

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

def sendMsg():
    while True:
        msg = input()
        if not msg:
            s.close()
        s.send(msg.encode('UTF-8'))

def listen():
    while True:
        msg = s.recv(1024).decode('UTF-8')
        if not msg:
            s.close()
        print("{0}: {1}".format(partner, msg))

def waitForLink():
    print('linking')
    while True:
        linked = s.recv(1024).decode('UTF-8')
        if linked == 'linked':
            return

def waitForPartner():
    print('waiting for partner')
    while True:
        partner = s.recv(1024).decode('UTF-8')
        if partner:
            return partner

waitForLink()
name = input('Choose username: ')
s.send(name.encode('UTF-8'))

partner = waitForPartner()
print('you are connected with %s'%partner)

send = Thread(target=sendMsg)
receive = Thread(target=listen)
send.start()
receive.start()
