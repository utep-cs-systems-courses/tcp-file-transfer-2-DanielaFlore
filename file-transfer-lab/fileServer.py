# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:13:54 2020

@author: Daniela Flores

TODO: write textfile on servers dir, implement fork()
"""

#! /usr/bin/env python3

# Echo server program

import socket, sys, re
from sockHelpers import sendAll

sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "fileserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
fileName = conn.recv(1024).decode()
print("filename is ", fileName)
conf = "filename received and stored"
sendAll(conn, conf.encode())
while 1:
    data = conn.recv(1024).decode()
    if not data: break
    sendMsg = f"Echoing <{data}>" 
    #print(f"Received <{data}>, sending <{sendMsg}>")
    sendAll(conn, sendMsg.encode())
conn.close()