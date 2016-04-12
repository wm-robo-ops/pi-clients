#!/usr/bin/env python


import sys
import time
import socket
import netifaces as ni


host = "192.168.1.132"
port = 8000

#log outputs
def writeToLog(the_string):
    f = open("/home/pi/robo-ops/pi-clients/server_listener.log", "a")
    f.write(the_string + "\n")
    f.close()

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    #find my ip
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[2][0]['addr']
    send(ip + "~", s)
    return s

def send(a_str, s):
    s.sendall(a_str)

if (len(sys.argv) < 2):
    print(sys.argv[0])
    print("video: server_ip")
    writeToLog("video: server_ip")
    sys.exit(1)

host = str(sys.argv[1])
print("video: connecting to server with ip: " + str(host) + " and port: " + str(port))
writeToLog("video: connecting to server with ip: " + str(host) + " and port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = 0

while True:

    #try to connect socket
    while isConnected == 0:
        try:
            s = connect()
            isConnected = 1
            print("video: connected to server")
            writeToLog("video: connected to server")

        except socket.error:
            time.sleep(1)
            s.close()
            isConnected = 0
            break

    while True:
        #try to send data
        try:
            data_pipe = open('/home/pi/robo-ops/pi-clients/outpipe', 'r', 0)
            read = None
            while sys.stdin != "":
                read = data_pipe.read(1024)
                send(read, s)

        except socket.error:
            s.close()
            isConnected = 0
            break

s.close()
