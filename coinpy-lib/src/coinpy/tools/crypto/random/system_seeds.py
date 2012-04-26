# -*- coding:utf-8 -*-
"""
Created on 25 Apr 2012

@author: kris
"""
import os

if os.name == 'nt':
    from coinpy.tools.crypto.random.perfmon import get_perfmon_data
    from coinpy.tools.crypto.random.performance_counter import get_performance_counter
    
    """ Get a list of (random_data, entropy) tuples suitable for ssl.RAND_add """
    def get_system_seeds():
        perfmon = get_perfmon_data() 
        perf_counter = get_performance_counter() 
        return [(perfmon, len(perfmon) / 100.0),
                (perf_counter, 1)]
else:
    pass
