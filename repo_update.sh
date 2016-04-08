#!/usr/bin/env bash

until bash /home/pi/robo-ops/pi-clients/if_wifi_on.sh
do
    echo "Wifi not connected"
    sleep 1
done
    
git -C /home/pi/robo-ops/pi-clients/ pull 
