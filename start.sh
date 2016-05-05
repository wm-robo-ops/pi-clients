#!/usr/bin/env bash

# Primary
server=ec2-54-85-173-111.compute-1.amazonaws.com
# Secondary
server=ec2-54-83-155-188.compute-1.amazonaws.com

sudo chown pi:pi *.sh *.py
sudo chown -R pi:pi .git

rm /home/pi/robo-ops/pi-clients/server_listener.log
bash /home/pi/robo-ops/pi-clients/repo_update.sh
python /home/pi/robo-ops/pi-clients/server-listener.py $server &
