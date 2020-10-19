#! /usr/bin/env python3

import sys,os
sys.path.append("../lib")       # for params
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)

while True:
    print("listening on:", bindAddr)
    
    sock, addr = lsock.accept()
    rc =os.fork()
    if rc < 0:
        print("fork failed")
        sys.exit(1)
    if rc == 0: #child
        print("forking success")
        print("connection rec'd from", addr)
        from framedSock import framedSend, framedReceive
        #################################################
        fileName = framedReceive(sock, debug).decode()
        print("filename is ", fileName)
        conf = "filename received and stored"
        framedSend(sock, conf.encode(), debug)
        path = os.getcwd()
        filesPath=path+'/'+fileName
        print(filesPath)
        if(os.path.isfile(filesPath)):
            print("file already exists in server....exiting")
            framedSend(sock, b"file exists", debug)
            sys.exit(0)
        framedSend(sock, b"pass", debug)
        f = open(fileName, "w")
        ################################################
    
        print("starting to write file....")
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if payload == b"end of file":
                closing = "end of file reached!"
                framedSend(sock, closing.encode(), debug)
                f.close()
                break
            f.write(payload.decode())
    
            if not payload:
                f.close()
                break
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)
        break #for child
print("end")
