#!/usr/bin/env bash

sudo pkill python
sudo pkill ffmpeg
rm /home/pi/robo-ops/pi-clients/server_listener.log
sudo bash /home/pi/robo-ops/pi-clients/repo_update.sh
python /home/pi/robo-ops/pi-clients/server-listener.py ec2-54-85-173-111.compute-1.amazonaws.com &
