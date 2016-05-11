	#!/usr/bin/env bash

#sudo pkill python
sudo pkill -9 -f start_video.py
sudo pkill -9 -f start_gps.py
sudo pkill -9 -f dof_device.py
sudo pkill -9 -f server-listener.py
sudo pkill ffmpeg
sudo /home/pi/robo-ops/pi-clients/start.sh
