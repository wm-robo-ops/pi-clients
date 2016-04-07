#!/usr/bin/env bash

PID=`pidof pigpiod`

if [ -z $PID ]; then
    sudo pigpiod
fi

../servos/setPos $1 $2
