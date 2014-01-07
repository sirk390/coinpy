from coinpy.tools.seeds.system_seeds import get_system_seeds,\
    ssl_add_system_seeds
from coinpy.tools.ssl.ssl import ssl_RAND_add, ssl_RAND_bytes

class Random():
    def __init__(self):
        ssl_add_system_seeds()
        
    def get_random_bytes(self, length):
        return ssl_RAND_bytes(length)

if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    
    r = Random()
    print hexstr(r.get_random_bytes(100))
