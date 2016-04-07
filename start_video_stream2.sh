#!/usr/bin/env bash

#ip='http://192.168.1.132'
ip=$2
port='8000'
width=320
height=240

echo "start_video_stream: starting video stream with server ip: $ip and port: $port"

sudo modprobe bcm2835-v4l2
rm outpipe
mkfifo outpipe
ffmpeg -loglevel fatal -threads 6 -s $width'x'$height -f video4linux2 -i /dev/video0 -f mpeg1video -b:v 400k -strict -1 -r $1 pipe:1 > /home/pi/robo-ops/pi-clients/outpipe &
/home/pi/robo-ops/pi-clients/start_video.py $ip
