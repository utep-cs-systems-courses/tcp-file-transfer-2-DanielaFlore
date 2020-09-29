# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:05:55 2020

@author: Daniela Flores:)
    
"""
#! /usr/bin/env python3

from sockHelpers import sendAll

# Echo client program
import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)
if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)
############################################
print("please write name of file you want to transfer to server(include extension i.e: .txt)")
fileName= input()
try:
    with open(fileName, 'r') as fl:
         allLines = fl.readlines()
         if len(allLines) == 0:
             print("file's empty....exiting")
             sys.exit(0)
except FileNotFoundError:
    print("no such file or directory")
    sys.exit(1)    
############################################
if s is None:
    print('could not open socket')
    sys.exit(1)


print("sending file name: '%s'" % fileName)
sendAll(s, fileName.encode())

data = s.recv(1024).decode()
print("Received '%s'" % data)

print("*************sending file contents!*****************")
for i in allLines:
    i = i.encode()
    sendAll(s,i)
    #print("file line:%s"%i)
#sendAll(s, allLines)

s.shutdown(socket.SHUT_WR)      # no more output

while 1:
    data = s.recv(1024).decode()
    #print("Received '%s'" % data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")


s.close()

