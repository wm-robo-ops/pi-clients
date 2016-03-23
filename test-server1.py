#!/usr/bin/env python

import sys
import socket
import os


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi_address = ("localhost", 12000)
s.connect(pi_address)

try:
    s.sendall("127.0.0.1|")

finally:
    s.close()
