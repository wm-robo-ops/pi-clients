#!/usr/bin/env python
import sys
import socket
import os
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi_address = ("localhost", 4000)
s.bind(pi_address)
s.listen(1)

connection, client_address = s.accept()
time.sleep(40)
connection.close()
s.close()
