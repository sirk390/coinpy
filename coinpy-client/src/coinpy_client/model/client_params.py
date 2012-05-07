# -*- coding:utf-8 -*-
"""
Created on 17 Mar 2012

@author: kris
"""

class ClientParams():
    """Client configuration parameters 
    
    List of parameters:
            data_directory: string
            runmode: MAIN/TESTNET
            port: int
            nonce: bignum
            sub_version_num: string
            targetpeers:int 
            logfilename: string
            seeds: list of SockAddr() 
            findpeers: boolean      use get_addr and bootstrap to find more peers
            bootstrap: boolean      use bootstraping
    """
    def __init__(self, **kwargs):
        self.parameters = kwargs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
            
    def load(self, client_params):
        for k, v in client_params.parameters.iteritems():
            self.parameters[k] = v
            setattr(self, k, v)
    
    def set(self, **kwargs):
        for param, value in kwargs.iteritems():
            self.parameters[param] = value
            setattr(self, param, value)

    def get(self, param, default):
        return self.parameters.get(param, default)

