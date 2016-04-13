#!/usr/bin/env bash

rm /home/pi/robo-ops/pi-clients/server_listener.log
bash /home/pi/robo-ops/pi-clients/repo_update.sh
python /home/pi/robo-ops/pi-clients/server-listener.py ec2-54-172-2-230.compute-1.amazonaws.com &
