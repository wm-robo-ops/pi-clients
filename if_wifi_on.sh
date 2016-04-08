#!/usr/bin/env bash

hits=`ifconfig | grep -o inet\ addr | wc -l`

#echo "$hits"

if [ $hits = 2 ]; then
exit 0
else 
exit 1
fi

