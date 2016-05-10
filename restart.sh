#!/usr/bin/env bash

#sudo pkill python
pkill -9 -f start_video.py
pkill -9 -f start_gps.py
pkill -9 -f dof_device.py
pkill -9 -f server-listener.py
sudo pkill ffmpeg
sudo /home/pi/robo-ops/pi-clients/start.sh
