# -*- coding:utf-8 -*-
"""
Created on 16 Nov 2011

@author: kris
"""
import itertools

''' 
    Enhanced version of itertools.groupby that sorts and returns a dictionary
'''
def xgroupby(data, keyfunc):
    data = sorted(data, key=keyfunc)
    return dict((grp, list(elemens)) for grp, elemens in itertools.groupby(data, keyfunc))

if (__name__ == '__main__'):
    print xgroupby(range(10), lambda x: x%5)
