#!/usr/bin/env python

import socket
import os

pid = {
	"VIDEO_STREAM": False,
	"DIRECTION_STREAM": False,
	"GPS_STREAM": False
}

command = {
	"VIDEO_STREAM": "./start_video_stream.sh",
	"DIRECTION_STREAM": "./dofdevice.py",
	"GPS_STREAM": "..."
}

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "100.91.29.141"
	port = 9998
	s.connect((host, port))
	return s

def send(a_str, s):
	s.send(a_str.encode())

def recieve(s):
	print("waiting")
	command = ''
	command = s.recv(1024).decode()
	print (command)
	return command


def start_process(input_str):
	#try:
		process = input_str.split("|")
		args = process[0].split(":")
		
		if (len(args) < 2):
			return

		start_stop = args[0]
		the_command = args[1]
		#start process
		if (start_stop == "START"):
			if (pid[the_command] == False):
				process_args = [command[the_command]]
				if (len(args) > 2):
					for i in range (2, len(args)):
						process_args.append(args[i])
		
				the_pid = os.fork()
				#child
				if the_pid == 0:
					os.execl(command[the_command], *tuple(process_args))
					assert False, 'error starting procces'
				#parent
				else:
					pid[the_command] = the_pid
					return
		
		elif (start_stop == "STOP"):
			if (pid[the_command] != False):
				kill = "kill -9 " + str(pid[the_command])
				os.system(kill)
				pid[the_command] = False
	#except:
	#	print("error in start_process")
	


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
			a_command = None
			a_command = recieve(s)
			if a_command != None and a_command != "":
				start_process(a_command)
			else:
				isConnected = 0
				break
			#print("Test")
			#start_process("test.py;|")
			#exit(0)		
		
		except socket.error:
			s.close()
			isConnected = 0
			break
s.close()
