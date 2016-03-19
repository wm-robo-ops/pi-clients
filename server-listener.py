#!/usr/bin/env python

import socket
import os


#dictionaries for processes
pid = {
    "VIDEO_STREAM": False,
    "DIRECTION_STREAM": False,
    "GPS_STREAM": False
}

command = {
    "VIDEO_STREAM": "/home/pi/robo-ops/pi-clients/start_video_stream.sh",
    "DIRECTION_STREAM": "/home/pi/robo-ops/pi-clients/dofdevice.py",
    "GPS_STREAM": "/home/pi/robo-ops/pi-clients/test.py",
    "PAN_TILT": "/home/pi/robo-ops/pi-clients/pan_tilt.sh"
}

# track current pan and tilt angles
curPan = 0
curTilt = 0

# host name and port number

host = "192.168.1.132"
port = 9998

#connect to server
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

#send string to socket
def send(a_str, s):
    s.send(a_str.encode())


#recieve data from socket
def recieve(s):
    print("waiting")
    command = ''
    command = s.recv(1024).decode()
    print (command)
    return command


#start process
def start_process(input_str):
    try:
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

        #stop process
        elif (start_stop == "STOP"):
            if (pid[the_command] != False):
                if (the_command == VIDEO_STREAM):
                    kill = "pkill ffmpeg"
                else:
                    kill = "kill -9 " + str(pid[the_command])

                os.system(kill)
                pid[the_command] = False

    except:
            print("error in start_process")



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

        except socket.error:
            s.close()
            isConnected = 0
            break
s.close()
