#!/usr/bin/env python

# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import sys
import time
import socket
import netifaces as ni

from Adafruit_BNO055 import BNO055

host = "192.168.1.132"
port = 3000

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
    s.sendall(a_str.encode())

if (len(sys.argv) < 2):
    print("dof: server_ip")
    writeToLog("dof: server_ip")
    sys.exit(1)

host = str(sys.argv[1])
print("dof: connecting to server with ip: " + str(host) + " and port: " + str(port))
writeToLog("dof: connecting to server with ip: " + str(host) + " and port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = 0
bno055 = 0

while True:

    #try to connect bno055
    while bno055 == 0:
        try:
            # Create and configure the BNO sensor connection.  Make sure only ONE of the
            # below 'bno = ...' lines is uncommented:
            # Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
            bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

            # BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
            # and RST connected to pin P9_12:
            #bno = BNO055.BNO055(rst='P9_12')


            # Enable verbose debug logging if -v is passed as a parameter.
            if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
                logging.basicConfig(level=logging.DEBUG)

            # Initialize the BNO055 and stop if something went wrong.
            if not bno.begin():
                raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

            # Print system status and self test result.
            status, self_test, error = bno.get_system_status()
            #print('System status: {0}'.format(status))
            #print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))

            # Print out an error if system status is in error mode.
            if status == 0x01:
                pass
                #print('System error: {0}'.format(error))
                #print('See datasheet section 4.3.59 for the meaning.')

            # Print BNO055 software revision and other diagnostic data.
            sw, bl, accel, mag, gyro = bno.get_revision()
            #print('Software version:   {0}'.format(sw))
            #print('Bootloader version: {0}'.format(bl))
            #print('Accelerometer ID:   0x{0:02X}'.format(accel))
            #print('Magnetometer ID:    0x{0:02X}'.format(mag))
            #print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
            #print('Reading BNO055 data, press Ctrl-C to quit...')

            #bno055 is connected
            bno055 = 1
            print("dof: device connected")
            writeToLog("dof: device connected")

        except:
            print("dof: error starting bno055")
            writeToLog("dof: error starting bno055")

    #try to connect socket
    while isConnected == 0:
        try:
            s = connect()
            isConnected = 1
            print("dof: connected to server")
            writeToLog("dof: connected to server")

        except socket.error:
            time.sleep(1)
            s.close()
            isConnected = 0
            break

        except:
            bno055 = 0
            break

    #if not connected restart loop to connect
    if (bno055 == 0):
        continue

    while True:
        #try to send data
        try:
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            heading, roll, pitch = bno.read_euler()
            # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
            sys, gyro, accel, mag = bno.get_calibration_status()
            # Print everything out.
            #print('Heading:{0:0.2F},Roll={1:0.2F},Pitch={2:0.2F}|'.format(
            #      heading, roll, pitch))
            send('heading:{0:0.2F},roll:{1:0.2F},pitch:{2:0.2F}|'.format(heading, roll, pitch), s)
            # Other values you can optionally read:
            # Orientation as a quaternion:
            #x,y,z,w = bno.read_quaterion()
            # Sensor temperature in degrees Celsius:
            #temp_c = bno.read_temp()
            # Magnetometer data (in micro-Teslas):
            #x,y,z = bno.read_magnetometer()
            # Gyroscope data (in degrees per second):
            x,y,z = bno.read_gyroscope()
            # Accelerometer data (in meters per second squared):
            #x,y,z = bno.read_accelerometer()
            # Linear acceleration data (i.e. acceleration from movement, not gravity--
            # returned in meters per second squared):
            #x,y,z = bno.read_linear_acceleration()
            # Gravity acceleration data (i.e. acceleration just from gravity--returned
            # in meters per second squared):
            #x,y,z = bno.read_gravity()
            # Sleep for a second until the next reading.
            time.sleep(.05)

        except socket.error:
            s.close()
            isConnected = 0
            break

        except:
            bno055 = 0
            break

s.close()
