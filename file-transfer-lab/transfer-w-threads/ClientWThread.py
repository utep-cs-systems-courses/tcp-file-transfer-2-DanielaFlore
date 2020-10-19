#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from encapFramedSock import EncapFramedSock


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

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)

sock.connect(addrPort)

fsock = EncapFramedSock((sock, addrPort))
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
fsock.send(fileName.encode(),debug)

#data = s.recv(1024).decode()
data =fsock.receive(debug)
print("Received '%s'" % data)
fExists = fsock.receive(debug)
if fExists == b"file exists":
    print("file already exists...exiting")
    sys.exit(0)
#f = open(fileName, "w")
print("*************sending file contents!*****************")

for i in allLines:
    i = i.encode()
    #framedSend(s,i,debug)
    fsock.send(i, debug)
    print("sending: ", i.decode())
    print("received:", fsock.receive(debug))
#added as a signal for server to close file being written
#framedSend(s, b"end of file", debug)
fsock.send(b"end of file", debug)
print("received:", fsock.receive(debug))
###################################################
