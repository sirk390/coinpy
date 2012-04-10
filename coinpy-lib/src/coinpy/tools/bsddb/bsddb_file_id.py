# -*- coding:utf-8 -*-
import struct

"""
Reads the 20 byte bytestring of a berkley database BTREE file.
Currently only supports version 3.2 (version=9)

See:Copying or moving databases
http://docs.oracle.com/cd/E17076_02/html/programmer_reference/program_copy.html

See structure of DBMETA (_dbmeta30, _dbmeta31)

See libdb source files:
    db_setid.c
    db_upgrade.h
    bt_upgrade.c

DB_BTREEMAGIC 0x53162

version mapping:
    version 7 => 3.0
    version 8 => 3.1
    version 9 => 3.2
"""

def bsddb_read_file_uid(fname):
    with open(fname, "rb") as f:
        dbmeta_part1 = f.read(20) # read dbmeta until version  
        magic,  = struct.unpack("<I", dbmeta_part1[12:16])
        version,  = struct.unpack("<I", dbmeta_part1[16:20])
        if magic != 0x53162:
            raise Exception ("bsddb btree file: incorrect magic : %d" % (magic))
        if version != 9:
            raise Exception ("bsddb file: unsupported version : %d" % (version))
        else:
            dbmeta_part2 = f.read(52)
            uid = dbmeta_part2[32:52]
            return uid
            
if __name__ == '__main__':
    
    fname = "d:\\repositories\\coinpy\\coinpy-client\\src\\coinpy_client\\data_testnet\\wallet_testnet.dat"
    fname2 = "d:\\repositories\\coinpy\\coinpy-client\\src\\coinpy_client\\data_testnet\\wallet_testnet2.dat"
    fname3 = "d:\\repositories\\coinpy\\coinpy-client\\src\\coinpy_client\\data_testnet\\wallet.dat"
    fname4 = "d:\\repositories\\coinpy\\coinpy-client\\src\\coinpy_client\\data_testnet\\wallet_testnet - Copy (9).dat"
    bsddb_read_file_uid(fname)
    bsddb_read_file_uid(fname2)
    bsddb_read_file_uid(fname3)
    bsddb_read_file_uid(fname4)
    