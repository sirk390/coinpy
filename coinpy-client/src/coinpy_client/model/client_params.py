# -*- coding:utf-8 -*-
"""
Created on 17 Mar 2012

@author: kris
"""
class ClientParams():
    def __init__(self, 
                 data_directory, 
                 runmode,
                 port, 
                 nonce,
                 sub_version_num,
                 targetpeers):
        self.data_directory = data_directory
        self.runmode = runmode
        self.port = port
        self.nonce = nonce
        self.sub_version_num = sub_version_num
        self.targetpeers = targetpeers