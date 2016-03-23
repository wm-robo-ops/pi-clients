#!/usr/bin/env bash

width=2592
height=1944

raspistill -w $width -h $height -t 200 -o /home/pi/robo-ops/pi-clients/pics/$1
