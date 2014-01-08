import struct
from coinpy.lib.wallet.formats.btc.file_model import ChunkHeader,\
     FileHeader, LogIndexEntry, ItemHeader, Log, Alloc
from coinpy.tools.functools import invert_dict
from coinpy.lib.wallet.formats.btc.wallet_model import PubKeyOutpoint,\
    MultiSigOutpoint, ScriptHashOutpoint, PublicKey, OutpointIndex
from coinpy.model.protocol.structures.uint256 import Uint256

class DeserializationException(Exception):
    pass

class Serializer(object):
    pass

def FixedSizeSerializer(size):
    class FixedSizeSerializerParam(Serializer):
        SERIALIZED_LENGTH = size
    return FixedSizeSerializerParam

class FileHeaderSerializer(FixedSizeSerializer(12)):
    SIGNATURE = "\x89WLT\r\n\x1a\n"
    @staticmethod
    def serialize(fileheader):
        return FileHeaderSerializer.SIGNATURE + struct.pack(">I", fileheader.version)
    @staticmethod
    def deserialize(data):
        if len(data) != FileHeaderSerializer.SERIALIZED_LENGTH:
            raise DeserializationException("File header has incorrect length: %s" % (len(data)))
        signature, version = data[:8], data[8:]
        if signature != FileHeaderSerializer.SIGNATURE:
            raise DeserializationException("Incorrect file signature: found %s instead of %s" % (signature, FileHeaderSerializer.SIGNATURE))
        return FileHeader(struct.unpack(">I", version))

class ChunkHeaderSerializer(FixedSizeSerializer(16)):
    @staticmethod
    def serialize(chunk_header):
        return struct.pack(">4sIII", 
                           chunk_header.name,
                           chunk_header.version,
                           chunk_header.length,
                           chunk_header.crc)
    @staticmethod
    def deserialize(data):
        if len(data) != ChunkHeaderSerializer.SERIALIZED_LENGTH:
            raise DeserializationException("log index incorrect length: %s" % (len(data)))
        name, version, length, crc  = struct.unpack(">4sIII", data)
        return ChunkHeader(name, version, length, crc)

class LogSerializer(object):
    @staticmethod
    def serialize(log):
        return struct.pack(">II", log.address, len(log.data)) + log.data + log.original_data

    @staticmethod
    def deserialize(data):
        if len(data) < 8:
            raise DeserializationException("log incorrect length")
        address_length, write_data = data[:8], data[8:]
        address, length = struct.unpack(">II", address_length)
        if len(write_data) != length * 2:
            raise DeserializationException("log incorrect length")
        return Log(address, write_data[:length], write_data[length:])


class LogIndexEntrySerializer(object):
    VALUES_FOR_COMMAND = { LogIndexEntry.BEGIN_TX : 1,
                           LogIndexEntry.END_TX : 2,
                           LogIndexEntry.WRITE : 3,
                           LogIndexEntry.CHANGE_FILESIZE : 4}
    COMMANDS_FOR_VALUES = invert_dict(VALUES_FOR_COMMAND)
    SERIALIZED_LENGTH = 6
    
    @staticmethod
    def serialize(log_index):
        return struct.pack(">BIB", LogIndexEntrySerializer.VALUES_FOR_COMMAND[log_index.command],
                           log_index.argument,
                           1 if log_index.needs_commit else 0)

    @staticmethod
    def deserialize(data):
        if len(data) != LogIndexEntrySerializer.SERIALIZED_LENGTH:
            raise DeserializationException("log index incorrect length: %s" % (len(data)))
        cmdval, argument, needs_commit = struct.unpack(">BIB", data)
        if cmdval not in LogIndexEntrySerializer.COMMANDS_FOR_VALUES:
            raise DeserializationException("log index unknown command value: %s" % (cmdval))
        if needs_commit > 1:
            raise DeserializationException("needs_commit not in [0,1]")
        return (LogIndexEntry(LogIndexEntrySerializer.COMMANDS_FOR_VALUES[cmdval],
                              argument,
                              bool(needs_commit)))

class ItemHeaderSerializer(FixedSizeSerializer(9)):
    @staticmethod
    def serialize(item_header):
        return struct.pack(">BII", 
                           not item_header.empty,
                           item_header.id,
                           item_header.size)

    @staticmethod
    def deserialize(data):
        if len(data) != ItemHeaderSerializer.SERIALIZED_LENGTH:
            raise DeserializationException("item_header incorrect length: %s" % (len(data)))
        empty, id, size = struct.unpack(">BII", data)
        return (ItemHeader(not empty, id, size))

class AllocSerializer(FixedSizeSerializer(5)):
    @staticmethod
    def serialize(item_header):
        return struct.pack(">BI", 
                           not item_header.empty,
                           item_header.size)

    @staticmethod
    def deserialize(data):
        if len(data) != AllocSerializer.SERIALIZED_LENGTH:
            raise DeserializationException(" Alloc incorrect length: %s" % (len(data)))
        empty, size = struct.unpack(">BI", data)
        return (Alloc(not empty, size))





class PubKeyOutpointSerializer(object):
    @staticmethod
    def serialize(outpoint):
        return outpoint.public_key.to_bytestr()

    @staticmethod
    def deserialize(data, outpoint_type):
        is_pubkey_hash = (outpoint_type == OutpointIndex.PUBKEY_HASH)
        return PubKeyOutpoint(PublicKey.from_bytestr(data), is_pubkey_hash=is_pubkey_hash)

class MultiSigOutpointSerializer(object):
    @staticmethod
    def serialize(outpoint):
        n_m =  struct.pack(">II", outpoint.n,
                                  outpoint.m)
        return (n_m +
                "".join(pubkey.to_bytestr() for pubkey in outpoint.public_key_list))

    @staticmethod
    def deserialize(data):
        n_m_data, public_keys_data = data[:8], data[8:]
        n, m  =  struct.unpack(">II", n_m_data)
        if len(public_keys_data) != m * 33:
            raise Exception("incorrect size")
        return MultiSigOutpoint(n, m, [PublicKey.from_bytestr(public_keys_data[i*33:i*33+33]) for i in range(m)])

                                     
class ScriptHashOutpointSerializer(object):
    pass

      
class OutpointIndexSerializer(object):
    OUTPOINT_TYPE_VALUES = {OutpointIndex.PUBKEY: 1, 
                            OutpointIndex.PUBKEY_HASH: 2, 
                            OutpointIndex.MULTISIG: 3, 
                            OutpointIndex.SCRIPT_HASH: 4}
    OUTPOINT_TYPES = invert_dict(OUTPOINT_TYPE_VALUES)
    @staticmethod
    def serialize(outpoint_index):
        header =  struct.pack(">I32sBBI", outpoint_index.id,
                                          outpoint_index.hash.to_bytestr_be(),
                                          outpoint_index.index,
                                          OutpointIndexSerializer.OUTPOINT_TYPE_VALUES[outpoint_index.type],
                                          outpoint_index.masterkey_id)
        if (outpoint_index.type == OutpointIndex.PUBKEY or 
            outpoint_index.type == OutpointIndex.PUBKEY_HASH):
            outpoint_data = PubKeyOutpointSerializer.serialize(outpoint_index.outpoint)
        elif outpoint_index.type == OutpointIndex.MULTISIG:
            outpoint_data = MultiSigOutpointSerializer.serialize(outpoint_index.outpoint)
        elif outpoint_index.type == OutpointIndex.SCRIPT_HASH:
            outpoint_data = ScriptHashOutpointSerializer.serialize(outpoint_index.outpoint)
        return header + outpoint_data

    @staticmethod
    def deserialize(data):
        length = struct.calcsize(">I32sBBI")
        if len(data) < length:
            raise Exception("size too small")
        index_data, outpoint_data = data[:length], data[length:]
        id, hash, index, type_value, masterkey_id   = struct.unpack(">I32sBBI", index_data)
        if type_value not in OutpointIndexSerializer.OUTPOINT_TYPES:
            raise Exception("unknown outpoint type: %d" % (type_value))
        oupoint_type = OutpointIndexSerializer.OUTPOINT_TYPES[type_value]
        if (oupoint_type == OutpointIndex.PUBKEY or 
            oupoint_type == OutpointIndex.PUBKEY_HASH):
            outpoint = PubKeyOutpointSerializer.deserialize(outpoint_data, oupoint_type == OutpointIndex.PUBKEY_HASH)
        elif oupoint_type == OutpointIndex.MULTISIG:
            outpoint = MultiSigOutpointSerializer.serialize(outpoint_data)
        elif oupoint_type == OutpointIndex.SCRIPT_HASH:
            outpoint = ScriptHashOutpointSerializer.serialize(outpoint_data)
        return OutpointIndex(id, Uint256.from_bytestr_be(hash), index, oupoint_type, masterkey_id, outpoint)
    




    