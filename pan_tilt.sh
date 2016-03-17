#!/usr/bin/env bash

if (!(pidof pigpiod)) then
sudo pigpiod
fi

../servos/setPos $1 $2
