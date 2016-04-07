#!/usr/bin/env python
import sys
import socket
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi_address = ("localhost", 9998)
s.bind(pi_address)
s.listen(1)

connection, client_address = s.accept()
connection.sendall("START:DIRECTION_STREAM|")

connection.close()
s.close()
