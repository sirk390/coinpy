# -*- coding:utf-8 -*-
"""
Created on 23 Apr 2012

@author: kris
"""
import asyncore
import socket
from coinpy.tools.reactor.reactor import Reactor, reactor
from coinpy.tools.reactor.asyncore_plugin import AsyncorePlugin

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)
            
class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

server = EchoServer('localhost', 8080)
reactor.install(AsyncorePlugin())
reactor.run()    
