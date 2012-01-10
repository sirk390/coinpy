# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
STATUS_OK, STATUS_ERROR = range(2)

class ValidationResult():
    
    
    def __init__(self, status, message="OK"):
        self.status = status
        self.message = message