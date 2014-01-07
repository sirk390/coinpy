import os
from coinpy.tools.ssl.ssl import ssl_RAND_add

if os.name == 'nt':
    from coinpy.tools.seeds.perfmon import get_perfmon_data
    from coinpy.tools.seeds.performance_counter import get_performance_counter
    
    """ Get a list of (random_data, entropy) tuples suitable for ssl.RAND_add """
    def get_system_seeds():
        perfmon = get_perfmon_data() 
        perf_counter = get_performance_counter() 
        return [(perfmon, len(perfmon) / 100.0),
                (perf_counter, 1)]
else:
    pass


def ssl_add_system_seeds():
    for data, entropy in get_system_seeds():
        ssl_RAND_add(data, entropy)
