# -*- coding:utf-8 -*-
"""
Created on 16 Apr 2012

@author: kris
"""

import unittest
from coinpy.node.node import Node
from coinpy.tools.reactor.reactor import Reactor
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
from coinpy.model.protocol.runmode import MAIN
from coinpy.node.network.sockaddr import SockAddr
from coinpy.model.protocol.messages.verack import VerackMessage
from coinpy.model.protocol.messages.types import MSG_VERACK

class TestBasicNode(unittest.TestCase):
    def setUp(self):
        pass
    def test_basic_node(self):
        pass

if __name__ == '__main__':
    unittest.main()
          