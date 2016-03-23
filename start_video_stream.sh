#!/usr/bin/env bash

#ip='http://192.168.1.132'
ip=$2
port='8082'
width=320
height=240

echo "start_video_stream: starting video stream with server ip: $ip and port: $port"

sudo modprobe bcm2835-v4l2
ffmpeg -threads 6 -s $width'x'$height -f rawvideo -pix_fmt yuv420p -i /dev/video0 -f mpeg1video -b:v 400k -strict -1 -r $1 http://$ip:$port
