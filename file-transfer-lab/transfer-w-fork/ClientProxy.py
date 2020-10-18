#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

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
print("sending file name: '%s'" % fileName)
fileName = "CreateAndDestroypt2.txt"
framedSend(s, fileName.encode(),debug)

#data = s.recv(1024).decode()
data =framedReceive(s, debug)
print("Received '%s'" % data)
fExists = framedReceive(s, debug)
if fExists == b"file exists":
    print("file already exists...exiting")
    sys.exit(0)
print("*************sending file contents!*****************")


for i in allLines:
    i = i.encode()
    framedSend(s,i,debug)
    print("sending: ", i.decode())
    print("received:", framedReceive(s, debug))
#added as a signal for server to close file being written
framedSend(s, b"end of file", debug)
print("received:", framedReceive(s, debug))
###################################################
