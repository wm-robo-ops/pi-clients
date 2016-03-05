#!/usr/bin/env python

import socket

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "100.91.29.141"
	port = 9000
	s.connect((host, port))
	return s

def send(a_str, s):
	s.send(a_str.encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = 0
while True:
	while isConnected == 0:
		try:
			s = connect()
			isConnected = 1
		except socket.error:
			isConnected = 0
	while True:
		try:
			send("test", s)
		
		except socket.error:
			s.close()
			isConnected = 0
			break
s.close()
