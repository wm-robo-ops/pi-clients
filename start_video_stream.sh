#!/usr/bin/env bash

ip='http://192.168.1.132'
port='8082'
width=320
height=240

sudo modprobe bcm2835-v4l2
ffmpeg -s $width'x'$height -f rawvideo -pix_fmt yuv420p -i /dev/video0 -f mpeg1video -b:v 800k -strict -1 -r $1 $ip:$port
