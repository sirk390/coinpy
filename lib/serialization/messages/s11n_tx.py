# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.structures.s11n_tx_out import tx_out_encoder
from coinpy.lib.serialization.structures.s11n_tx_in import tx_in_encoder
from coinpy.model.protocol.messages.tx import msg_tx
from coinpy.lib.serialization.structures.s11n_tx import tx_encoder

class tx_msg_encoder(Encoder):
    def __init__(self):    
        self.txencoder = tx_encoder()
     
    def encode(self, txmsg):
        return (self.txencoder.encode(txmsg.tx))

    def decode(self, data, cursor=0):
        tx, cursor = self.txencoder.decode(data, cursor)
        return (msg_tx(tx), cursor)

