#!/usr/bin/env python

import socket
import os

port = 12000


def send(a_str, s):
    s.send(a_str.encode())

def listen(s):
    #bind port
    pi_address = ("localhost", port)
    print ("listening on port " + str(pi_address[1]))
    s.bind(pi_address)
    s.listen(1)

    while True:
        #accept incoming conection
        connection, client_address = s.accept()

        try:
            #recieve ip adress of server
            server_ip = ""
            data = ""
            while (data != "|"):
                server_ip += data
                data = connection.recv(1)
            
            print("starting server-listener with server ip: " + str(server_ip))
            
            the_pid = os.fork()
            #child
            if the_pid == 0:
                args = ("/home/pi/robo-ops/pi-clients/server-listener.py", server_ip)
                os.execl( args[0], *args)
                assert False, 'start.py: error starting server-listener'
            #parent
            else:
                #wait for child to end
                os.waitpid(the_pid, 0)

        finally:
            connection.close()

#create the socket and listen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen(s);

