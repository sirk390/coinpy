# -*- coding:utf-8 -*-
"""
Created on 7 Jan 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import TARGET_INTERVAL

def get_next_work_required(blockref, block):
    if ((blockref.height  + 1) % TARGET_INTERVAL):
        #same difficulty
        return (blockref.blockheader.bits)
    #recompute difficulty
    startref = blockref
    for i in range(INTERVAL):
        startref = startref
        