#!/usr/bin/env bash

sudo pkill python
sudo pkill ffmpeg
rm /home/pi/robo-ops/pi-clients/server_listener.log
sudo bash /home/pi/robo-ops/pi-clients/repo_update.sh
sudo python /home/pi/robo-ops/pi-clients/server-listener.py ec2-54-172-2-230.compute-1.amazonaws.com
