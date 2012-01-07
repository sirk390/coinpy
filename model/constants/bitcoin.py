# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""

COIN = 100000000
CENT = 1000000
MAX_MONEY = 21000000 * COIN

TARGET_TIMESPAN =  14 * 24 * 60 * 60 # 2 weeks
TARGET_SPACING = 10 * 60 # 10 minutes
TARGET_INTERVAL = TARGET_TIMESPAN / TARGET_SPACING #  2016 blocks / 2weeks

def is_money_range(value):
    return (value >= 0 and value <= MAX_MONEY)
