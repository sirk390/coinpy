import ctypes
import ctypes.util

#ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('libeay32'))
ssl = ctypes.cdll.LoadLibrary (r'c:\programs\python27\libeay32.dll')

#EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha512()
"""
EVP_DecryptUpdate = ssl.EVP_DecryptUpdate
EVP_DecryptUpdate.argtypes = [ctypes.c_char_p, ctypes.POINTER]
"""

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

    