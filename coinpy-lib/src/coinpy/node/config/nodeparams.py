# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
from coinpy.model.protocol.runmode import MAIN

class NodeParams(object):
    """
        Static parameters for the bitcoin node.
    """
    def __init__(self,
                 runmode=MAIN,
                 port = 8080,
                 version = 209,
                 enabledservices=SERVICES_NODE_NETWORK,
                 nonce=0,
                 sub_version_num="mybitcoin",
                 targetpeers=5,
#    The below parameters limit the number of allowed sig_op per transaction script.
#    
#    Verifying ECDSA signatures is very CPU intensive so setting this parameter 
#    too high can allow CPU DOS attacks by spamming transactions.
#
#    script_max_sig_op_count:
#            Maximum number of OP_CHECKSIG, OP_CHECKSIGVERIFY per script.
#   
#    script_max_multisig_op_count:
#             Maximum number of OP_CHECKMULTISIG, OP_CHECKMULTISIGVERIFY:
#
                 max_script_sig_op_count=1,
                 max_script_multisig_op_count=0,
                 allow_non_standard_scripts=False
                 
                 
                 ):
        self.runmode = runmode
        self.port = port
        self.version = version
        self.enabledservices = enabledservices
        self.nonce = nonce
        self.sub_version_num = sub_version_num
        self.targetpeers = targetpeers
        
        self.max_script_sig_op_count = max_script_sig_op_count
        self.max_script_multisig_op_count = max_script_multisig_op_count
        self.allow_non_standard_scripts = allow_non_standard_scripts
        
        
