# -*- coding:utf-8 -*-
"""
Created on 16 Apr 2012

@author: kris
"""

import unittest
from coinpy.node.node import Node
from coinpy.tools.reactor.reactor import Reactor, reactor
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
from coinpy.model.protocol.runmode import MAIN
from coinpy.tools.log.basic_logger import stdout_logger
from coinpy.node.network.sockaddr import SockAddr
from coinpy.model.protocol.messages.verack import VerackMessage
from coinpy.model.protocol.messages.types import MSG_VERACK

class TestNode(unittest.TestCase):
    def setUp(self):
        pass
    """Create two instances of 'Node' and connect from the first to the second"""
    def test_node_connect_accept(self):
        log = stdout_logger()
        params1 = NodeParams(runmode=MAIN, port=8333)
        params2 = NodeParams(runmode=MAIN, port=8334)
        
        node1 = Node(params1, log)
        node2 = Node(params2, log)
        node1.connect_peer(SockAddr("localhost", 8334))
        node2.subscribe(Node.EVT_CONNECTED, lambda event: reactor.stop())
        reactor.run()

    """Create two instances of 'Node', connect and send a Verack Message"""
    def test_node_send_receive_message(self):
        log = stdout_logger()
        params1 = NodeParams(runmode=MAIN, port=8335)
        params2 = NodeParams(runmode=MAIN, port=8336)
        
        node1 = Node(params1, log)
        node2 = Node(params2, log)
        def on_connect(event):
            node1.send_message(event.handler, VerackMessage())
        node1.subscribe(Node.EVT_CONNECTED, on_connect)
        
        def on_message(event):
            assert event.message.type == MSG_VERACK
            reactor.stop()
        node2.subscribe(Node.EVT_BASIC_MESSAGE, on_message)
        node1.connect_peer(SockAddr("localhost", 8336))
        
        reactor.run()

if __name__ == '__main__':
    unittest.main()
          