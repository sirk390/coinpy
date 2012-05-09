# -*- coding:utf-8 -*-
"""
Created on 9 May 2012

@author: kris
"""
import socket
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.network.bitcoin_port import BITCOIN_PORT

DNS_SEEDS = [
    "bitseed.xf2.org",
    "dnsseed.bluematt.me",
    "seed.bitcoin.sipa.be",
    "dnsseed.bitcoin.dashjr.org"
]

def dns_seeds(runmode):
    sockaddrs = []
    for s in DNS_SEEDS:
        try:
            ip = socket.gethostbyname(s)
        except:
            pass
        sockaddrs.append(SockAddr(ip, BITCOIN_PORT[runmode]))
    return sockaddrs

if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN
    print dns_seeds(MAIN)