# -*- coding: utf-8 -*-
"""

@author: Daniela Flores

TODO:  implement fork(), add comments
"""

#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
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
path = os.getcwd()
filesPath=path+'\\'+fileName
print(filesPath)
if(os.path.isfile(filesPath)):
    print("file already exists in server....exiting")
    conn.close()
    sys.exit(0)
f = open(fileName, "w")
while 1:
    data = conn.recv(1024).decode()
    f.write(data)
    if not data: break
    sendMsg = f"Echoing <{data}>" 
    #print(f"Received <{data}>, sending <{sendMsg}>")
    sendAll(conn, sendMsg.encode())
f.close()
conn.close()
