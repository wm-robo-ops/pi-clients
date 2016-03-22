#!/usr/bin/env python

import socket
import os

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
    s.sendall(a_str.encode())

def sendPic(file_name):
    try:
        f = open(file_name, 'r')
        pic_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pic_sock.connect((host, pic_port))

        # send file
        data = f.read(1024)
        while (data):
            pic_sock.sendall(data)
            data = f.read(1024)
        f.close()
        pic_sock.close()
        print("done sending pic")
    
    except:
        print("error in sendPic")



#recieve data from socket
def receive(s):
    print("waiting to receive command")
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
                    if (the_command != "CAPTURE_PHOTO"):
                        pid[the_command] = the_pid
                    else:
                        
                        while(not os.path.isfile("/home/pi/robo-ops/pi-clients/pics/" + str(process_args[len(process_args) - 1]))):
                            continue
                        
                        sendPic("/home/pi/robo-ops/pi-clients/pics/" + str(process_args[len(process_args) - 1]))

        #stop process
        elif (start_stop == "STOP"):
            if (pid[the_command] != False):
                if (the_command == "VIDEO_STREAM"):
                    kill = "sudo pkill ffmpeg"
                else:
                    kill = "sudo kill -9 " + str(pid[the_command])

                os.system(kill)
                pid[the_command] = False

    except:
        print("error in start_process")
    finally:
        return


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
            a_command = receive(s)

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
