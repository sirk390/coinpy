# -*- coding:utf-8 -*-
"""
Created on 2 Mar 2012

@author: kris
"""

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False