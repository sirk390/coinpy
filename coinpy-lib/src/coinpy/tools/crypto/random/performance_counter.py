# -*- coding:utf-8 -*-
"""
Created on 25 Apr 2012

@author: kris
"""
import os
import ctypes
import ctypes.util

if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32 
    def get_performance_counter():
        counter = ctypes.c_int64(0)
        e = kernel32.QueryPerformanceCounter(ctypes.byref(counter))
        return buffer(counter)[:]
else:
    pass
    """
    inline int64 GetPerformanceCounter()
    {
        int64 nCounter = 0;
    #ifdef WIN32
        QueryPerformanceCounter((LARGE_INTEGER*)&nCounter);
    #else
        timeval t;
        gettimeofday(&t, NULL);
        nCounter = t.tv_sec * 1000000 + t.tv_usec;
    #endif
        return nCounter;"""
if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    
    print hexstr(get_performance_counter())
    

