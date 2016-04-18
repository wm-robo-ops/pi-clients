#!/usr/bin/env python

import gps
import sys
import time
import socket
import netifaces as ni


host = "192.168.1.132"
port = 4000

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
    print("gps: server_ip")
    writeToLog("gps: server_ip")
    sys.exit(1)

host = str(sys.argv[1])
print("gps: connecting to server with ip: " + str(host) + " and port: " + str(port))
writeToLog("gps: connecting to server with ip: " + str(host) + " and port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = 0
session = None
gps_connected = 0

while True:

    #try to connect socket
    while isConnected == 0:
        try:
            s = connect()
            isConnected = 1
            print("gps: connected to server")
            writeToLog("gps: connected to server")

        except socket.error:
            time.sleep(1)
            s.close()
            isConnected = 0
            break

    #try to connect gps
    while gps_connected == 0:
#            try:
        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        gps_connected = 1
        
#except:
#            session = None
#            gps_connected = 0
#            print("gps: gps disconnected")
#            writeToLog("gps: gps disconnected")

    while True:
        #try to send data
        try:
            report = session.next()
            if report['class'] == 'TPV':
                lat = ''
                lon = ''
                if hasattr(report, 'lat'):
                    lat = report.lat
                if hasattr(report, 'lat'):
                    lon = report.lon
                send(("lat:" + str(lat) + ",lon:" + str(lon) + "|"), s)
                print("lat:" + str(lat) + ",lon:" + str(lon) + "|")


        except socket.error:
            s.close()
            isConnected = 0
            break
        
        except StopIteration:
            session = None
            gps_connected = 0
            print "gps: gps disconnected"
            writeToLog("gps: gps disconnected")
            break

#        except:
#            session = None
#            gps_connected = 0
#            s.close()
#            isConnected = 0
#            print("gps: something went wrong")
#            writeToLog("gps: something went wrong")
#            break

s.close()
