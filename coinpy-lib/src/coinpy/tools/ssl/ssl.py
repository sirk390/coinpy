import ctypes
import ctypes.util

ssl = ctypes.cdll.LoadLibrary (r'libeay32.dll')

def ssl_RAND_bytes(length):
    buffer = ctypes.create_string_buffer (length)
    ssl.RAND_bytes(buffer, length)
    return buffer.raw

def ssl_RAND_add(data, entropy):
    ssl.RAND_add(data, len(data), ctypes.c_double(entropy))
    
if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    
    ssl_RAND_add("hello", 5)
    print hexstr(ssl_RAND_bytes(10))

    