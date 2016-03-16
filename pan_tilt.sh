#!/usr/bin/env bash

if (!(pidof pigpiod) > 0) then
sudo pigpiod
fi

../servos/setPos $1 $2
