# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.model.protocol.services import SERVICES_NONE, SERVICES_NODE_NETWORK
from coinpy.model.protocol.structures.netaddr import netaddr
from coinpy.model.protocol.messages.types import MSG_VERSION, MSG_VERACK
from coinpy.model.protocol.messages.verack import msg_verack
from coinpy.model.protocol.messages.version import msg_version
import time
from coinpy.tools.observer import Observable
from coinpy.node.node import Node
from coinpy.node.logic.status.version_status import VersionStatus


class VersionExchangeNode(Node):
    EVT_VERSION_EXCHANGED = Observable.createevent()
            
    def __init__(self, reactor, get_blockchain_height, params, log):
        super(VersionExchangeNode, self).__init__(reactor, params, log)
        self.subscribe(Node.EVT_CONNECTED, self.__on_connected)
        
        self.get_blockchain_height = get_blockchain_height
        self.version_statuses = {}
        self.version_exchanged_nodes = set()

    def __on_connected(self, event):
        self.version_statuses[event.handler] = VersionStatus()
        if (event.handler.isoutbound):
            self.send_version(event.handler)
            
    def __on_version(self, event):
        status = self.version_statuses[event.source]
        status.version_received = True
        status.version_message = event.message
        self.log.info("received version (%s: %d)" % (str(event.source), event.message.version))
        if (not self.is_supported_version(event.message.version)):
            self.log.warning("version %d not supported" % (event.message.version))
            self.misbehaving(event.source, "version %d not supported" % (event.message.version))
            return
        self.send_verack(event.source)
        if (not event.source.isoutbound):
            self.send_version(event.source)
        self.check_version_exchanged(event.source)
        
    def __on_verack(self, event):
        self.log.info("received verack (%s)" % (str(event.source)))
        status = self.version_statuses[event.source]
        #if (not status.sent_version or status.verack_received):
        #    event.source.handle_close()
        #    return
        status.verack_received = True
        self.check_version_exchanged(event.source)

    def on_message(self, event):
        if (event.message.type == MSG_VERSION):
            self.__on_version(event)
            return
        if (event.message.type == MSG_VERACK):
            self.__on_verack(event)
            return
        if (event.handler not in self.version_exchanged_nodes):
            self.log.warning("peer %s sent message before message exchanging version" % (str(event.handler)))
            return
        self.fire_message_event(event.handler, event.message)
        
    def check_version_exchanged(self, handler):
        if self.version_statuses[handler].versions_exchanged():
            self.log.info("Accepted new peer: %s" % (handler))
            self.version_exchanged_nodes.add(handler)
            #todo: replace 'handler' by 'peer'
            self.fire(self.EVT_VERSION_EXCHANGED, handler=handler, version_message=self.version_statuses[handler].version_message)
          
    def send_version(self, handler):
        #todo: remove usage of node.params and node.addr_me
        version = msg_version(version = self.params.version, 
                     services=self.params.enabledservices, 
                     timestamp=time.time(), 
                     addr_me=self.addr_me, 
                     addr_you=netaddr(SERVICES_NONE, handler.sockaddr.ip, handler.sockaddr.port), 
                     nonce=self.params.nonce, 
                     sub_version_num=self.params.sub_version_num,
                     start_height=self.get_blockchain_height())
        self.log.info("Sending version(%s): %s" % (handler.sockaddr, version))
        self.version_statuses[handler].version_sent = True
        handler.send_message(version)

    def send_verack(self, handler):
        verack = msg_verack()
        self.log.info("Sending verack(%s): %s" % (handler.sockaddr, verack))
        self.version_statuses[handler].verack_sent = True
        handler.send_message(msg_verack()) 
         
    def is_supported_version(self, version):
        return (version >= 32000) #or 32200?


