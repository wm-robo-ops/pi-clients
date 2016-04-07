#!/usr/bin/env python

import socket
import os
import sys
import time
import netifaces as ni

#video on should be previous fps
video_on = 0

#dictionaries for processes
pid = {
    "VIDEO_STREAM": False,
    "DIRECTION_STREAM": False,
    "GPS_STREAM": False,
    "CAPTURE_PHOTO": False
}

command = {
    "VIDEO_STREAM": "/home/pi/robo-ops/pi-clients/start_video_stream2.sh",
    "DIRECTION_STREAM": "/home/pi/robo-ops/pi-clients/dof_device.py",
    "GPS_STREAM": "/home/pi/robo-ops/pi-clients/test.py",
    "CAPTURE_PHOTO": "/home/pi/robo-ops/pi-clients/take_pic.sh"
}

# host name and port number

host = "192.168.1.132"
port = 9000

pic_port = 7000

#connect to server
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("server-listener: connected to command server")
    #find my ip
    ni.ifaddresses('wlan0');
    ip = ni.ifaddresses('wlan0')[2][0]['addr']
    send(ip + "~", s)
    return s

#send string to socket
def send(a_str, s):
    s.sendall(a_str.encode())

#send a picture with given file name
def sendPic(file_name):
    try:
        f = open(file_name, 'r')
        pic_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pic_sock.connect((host, pic_port))
        
        print("server-listener: sending picture to server ip: " + str(host) + "port: " + str(port))
        
        # send file
        data = f.read(1024)
        while (data):
            pic_sock.sendall(data)
            data = f.read(1024)
        print("server-listener: done sending pic")
    
    except:
        print("server-listener: error in sendPic")

    finally:
        f.close()
        pic_sock.close()

#recieve data from socket
def receive(s):
    print("server-listener: waiting to receive command")
    command = ''
    data = ' '
    
    while (data != "|"):
        data = s.recv(1).decode()
        sys.stdout.write(data)
        if (len(data) == 0):
            break
        if (data != " "):
            command += data

    print ("server-listener: " + command)
    return command


#start process
def start_process(input_str):
#   try:
        global video_on
        process = input_str.split("|")
        args = process[0].split(":")

        if (len(args) < 2):
            return

        start_stop = args[0]
        the_command = args[1]

        #start process
        if (start_stop == "START"):
            if (pid[the_command] == False):
                if (the_command == "CAPTURE_PHOTO" and pid["VIDEO_STREAM"] != False):
                    os.system("/home/pi/robo-ops/pi-clients/stop_video.sh")
                    print("stopped video")
                    time.sleep(2)
                    #return
                process_args = [command[the_command]]
                if (len(args) > 2):
                    for i in range (2, len(args)):
                        process_args.append(args[i])
                
                #add host param if needed        
                if (the_command != "CAPTURE_PHOTO"):
                    process_args.append(str(host))
                
                #if we need to set video variable
                if (the_command == "VIDEO_STREAM"):
                    video_on = process_args[-2]

                the_pid = os.fork()
                #child
                if the_pid == 0:
                    os.execl(command[the_command], *tuple(process_args))
                    assert False, 'server-listener: error starting child procces'
                #parent
                else:
                    if (the_command != "CAPTURE_PHOTO"):
                        pid[the_command] = the_pid
                    else:
                        if (video_on != 0):
                            time.sleep(1)
                            #child
                            if (os.fork() == 0):
                                os.execl(command["VIDEO_STREAM"], *(command["VIDEO_STREAM"], video_on, host))
                                #start_process("START:VIDEO_STREAM:" + str(video_on) + "|")

                        while(not os.path.isfile("/home/pi/robo-ops/pi-clients/pics/" + str(process_args[len(process_args) - 1]))):
                            continue
                        
                        sendPic("/home/pi/robo-ops/pi-clients/pics/" + str(process_args[len(process_args) - 1]))

        #stop process
        elif (start_stop == "STOP"):
            if (pid[the_command] != False):
                if (the_command == "VIDEO_STREAM"):
                    #kill = "sudo pkill ffmpeg"
                    os.system("/home/pi/robo-ops/pi-clients/stop_video.sh")
                    video_on = 0
                else:
                    kill = "sudo kill -9 " + str(pid[the_command])
                    os.system(kill)
                
                #os.system(kill)
                pid[the_command] = False

#except:
#        print("server-listener: error in start_process")
#   finally:
#       return

time.sleep(10);

if (len(sys.argv) < 2):
    print("server-listener: server_ip")
    sys.exit(1)

host = str(sys.argv[1])
print("server-listener: starting with server ip: " + str(host) + " and port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = 0
while True:
    while isConnected == 0:
        try:
            s = connect()
            isConnected = 1

        except socket.error:
#s.close()
            isConnected = 0
    
    while True:
        try:
            a_command = None
            a_command = receive(s)
            sys.stdout.flush()
            if a_command != None and a_command != "":
                start_process(a_command)
            else:
                print("server-listener: disconnected from command server")
#s.close()
                isConnected = 0
                break

        except socket.error:
            print("server-listener: disconnected from command server")
            s.close()
            isConnected = 0
            break

s.close()
