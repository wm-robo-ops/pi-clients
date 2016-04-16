#!/usr/bin/env bash

rm /home/pi/robo-ops/pi-clients/server_listener.log
bash /home/pi/robo-ops/pi-clients/repo_update.sh
python /home/pi/robo-ops/pi-clients/server-listener.py ec2-54-85-173-111.compute-1.amazonaws.com &
