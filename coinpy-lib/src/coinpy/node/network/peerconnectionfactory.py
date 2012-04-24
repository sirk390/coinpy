# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from peerconnection import PeerConnection

class PeerConnectionFactory():
    def __init__(self, msg_encoder, log):
        self.msg_encoder = msg_encoder
        self.log = log
        
    def create_connection(self, sockaddr, sock=None):
        return PeerConnection(sockaddr, self.msg_encoder, sock, self.log)
