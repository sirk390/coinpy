# -*- coding:utf-8 -*-
"""
Created on 11 Feb 2012

@author: kris
"""
import bsddb
from bsddb.db import DB_CREATE, DB_INIT_LOCK, DB_INIT_LOG, DB_INIT_MPOOL, \
    DB_INIT_TXN, DB_THREAD, DB_RECOVER

class BSDDBEnv(object):
    def __init__(self, directory):
        self.directory = directory
        self.dbenv = bsddb.db.DBEnv()
        
        self.dbenv.set_lg_max(10000000)
        self.dbenv.set_lk_max_locks(10000)
        self.dbenv.set_lk_max_objects(10000)
        self.dbenv.open(directory,
                          DB_CREATE|DB_INIT_LOCK|DB_INIT_LOG|DB_INIT_MPOOL|
                           DB_INIT_TXN|DB_THREAD|DB_RECOVER)
