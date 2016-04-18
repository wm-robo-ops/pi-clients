#!/usr/bin/env bash

sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
python /home/pi/robo-ops/pi-clients/testing/start_gps.py

