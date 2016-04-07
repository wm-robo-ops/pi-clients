#!/usr/bin/env python

import socket

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "198.168.1.132"
    port = 9998
    s.connect((host, port))
    return s

def send(a_str, s):
    s.send(a_str.encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
while True:
    while not connected:
        try:
            s = connect()
            connected = True
        except socket.error:
            connected = False
    while True:
        try:
            send("test", s)

        except socket.error:
            s.close()
            connected = False
            break
s.close()
