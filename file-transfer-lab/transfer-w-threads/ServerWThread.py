#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

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
print("listening on:", bindAddr)

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            #payload = self.fsock.receive(debug)
            ###
            from framedSock import framedSend, framedReceive
            #################################################
            fileName = self.fsock.receive(debug).decode()
            print("filename is ", fileName)
            conf = "filename received and stored"
            #framedSend(sock, conf.encode(), debug)
            self.fsock.send(conf.encode(), debug)
            path = os.getcwd()
            #/
            filesPath=path+'\\'+fileName
            print(filesPath)
            if(os.path.isfile(filesPath)):
                print("file already exists in server....exiting")
                #framedSend(sock, b"file exists", debug)
                self.fsock.send(b"file exists", debug)
                sys.exit(0)
            self.fsock.send(b"pass", debug)
            f = open(fileName, "w")
            ################################################
        
            print("starting to write file....")
            while True:
                payload = self.fsock.receive(debug).decode()
                if debug: print("rec'd: ", payload)
                if payload == "end of file":
                    closing = "end of file reached!"
                    #framedSend(sock, closing.encode(), debug)
                    self.fsock.send(closing.encode(), debug)
                    #f.close()
                    self.fsock.close()
                    #break
                f.write(payload)
        
                if not payload:
                    self.fsock.close()
                    return
                payload += "!"             # make emphatic!
                self.fsock.send(payload.encode(), debug)
            break #for child



while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
