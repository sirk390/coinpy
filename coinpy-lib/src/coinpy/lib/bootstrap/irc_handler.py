# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.tools.observer import Observable
import asyncore
import socket
import traceback

RECV_SIZE=4096

class IrcHandler(asyncore.dispatcher_with_send, Observable):
    EVT_CONNECT = Observable.createevent()
    EVT_DISCONNECT = Observable.createevent()
    EVT_RECV_LINE = Observable.createevent()
   
    def __init__(self, reactor, log, sockaddr):
        Observable.__init__(self, reactor)
        asyncore.dispatcher_with_send.__init__(self)
        self.sockaddr = sockaddr
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(sockaddr)
        self.incommingbuff = ""
        self.log = log
            
    def handle_connect(self):
        self.fire(self.EVT_CONNECT)
        
    def readable(self):
        return (True)
    
    def handle_read(self):
        self.incommingbuff += self.recv(RECV_SIZE) 
        lines = self.incommingbuff.split("\r\n")
        completedlines, leftover = lines[:-1], lines[-1]
        for l in completedlines: 
            self.fire(self.EVT_RECV_LINE, line=l)
        self.incommingbuff = leftover

    def handle_error(self):
        self.log.error(traceback.format_exc())
                
    def handle_close(self):
        self.close()
        self.fire(self.EVT_DISCONNECT)
