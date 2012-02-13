# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
import logging
import sys

def createlogger(name="coinpy"):
    logger = logging.getLogger(name)
    #logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #'%(asctime)-15s %(clientip)s %(user)-8s %(message)s
    
    #File
    #hdlr = logging.FileHandler('/var/tmp/myapp.log')
    #hdlr.setFormatter(formatter)
    
    #Stdout
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(fmt)
    logger.addHandler(stdout)
    return logger


if __name__ == '__main__':
    log = createlogger()
    log.info("test")
    log.warning("warning")
