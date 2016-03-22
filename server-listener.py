#!/usr/bin/env python

import socket
import os

#pic number
pic_num = 0


#dictionaries for processes
pid = {
    "VIDEO_STREAM": False,
    "DIRECTION_STREAM": False,
    "GPS_STREAM": False,
    "CAPTURE_PHOTO": False
}

command = {
    "VIDEO_STREAM": "/home/pi/robo-ops/pi-clients/start_video_stream.sh",
    "DIRECTION_STREAM": "/home/pi/robo-ops/pi-clients/dofdevice.py",
    "GPS_STREAM": "/home/pi/robo-ops/pi-clients/test.py",
    "CAPTURE_PHOTO": "/home/pi/robo-ops/pi-clients/take_pic.sh"
}

# host name and port number

host = "192.168.1.132"
port = 9998

pic_port = 7777

#connect to server
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

#send string to socket
def send(a_str, s):
    s.send(a_str.encode())

def sendPic(file_name):
    f = open(file_name, 'r')
    pic_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pic_sock.connect((host, pic_port))
    data = f.read(1024)
    while (data):
        pic_sock.send(data)
        data = f.read(1024)
    f.close()
    pic_sock.close()
    print("done sending pic")

#recieve data from socket
def recieve(s):
    print("waiting")
    command = ''
    command = s.recv(1024).decode()
    print (command)
    return command


#start process
def start_process(input_str, pic_num):
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
                if (the_command == "CAPTURE_PHOTO"):
                    process_args.append(str(pic_num))
    
                the_pid = os.fork()
                #child
                if the_pid == 0:
                    os.execl(command[the_command], *tuple(process_args))
                    assert False, 'error starting procces'
                #parent
                else:
                    if (the_command != "CAPTURE_PHOTO"):
                        pid[the_command] = the_pid
                    else:
                        while(not os.path.isfile("/home/pi/robo-ops/pi-clients/pics/" + str(pic_num) + ".png")):
                            continue
                        sendPic("/home/pi/robo-ops/pi-clients/pics/" + str(pic_num) + ".png")
                    return

        #stop process
        elif (start_stop == "STOP"):
            if (pid[the_command] != False):
                if (the_command == "VIDEO_STREAM"):
                    kill = "pkill ffmpeg"
                else:
                    kill = "kill -9 " + str(pid[the_command])

                os.system(kill)
                pid[the_command] = False
       #except:
#    print("error in start_process")



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
                start_process(a_command, pic_num)
                pic_num += 1
            else:
                isConnected = 0
                break

        except socket.error:
            s.close()
            isConnected = 0
            break
s.close()
