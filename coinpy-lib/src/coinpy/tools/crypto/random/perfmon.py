# -*- coding:utf-8 -*-
"""
Created on 25 Apr 2012

@author: kris
"""
import os
import ctypes
import ctypes.util

if os.name == 'nt':
    import _winreg
    
    def get_perfmon_data():
        value, type = _winreg.QueryValueEx(_winreg.HKEY_PERFORMANCE_DATA, "Global")
        return value

if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    
    print hexstr(get_perfmon_data()[0:100])
    

