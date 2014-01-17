from coinpy.tools.event import Event
from coinpy.tools.hex import decodehexstr, hexstr
from collections import defaultdict

class MasterKey( object ):
    def __init__(self, id, comment, crypted_key, salt, deriv_method, derive_iterations):
        self.id = id
        self.comment = comment
        self.crypted_key = crypted_key
        self.salt = salt
        self.deriv_method = deriv_method
        self.derive_iterations = derive_iterations

class PrivateKey( object ):
    def __init__(self, id, masterkey_id=None, private_key_data=None):
        self.id = id
        self.masterkey_id = masterkey_id
        self.private_key_data = private_key_data

class PublicKey( object ):
    def __init__(self,  data=True):
        #internal representation: big endian 33 byte string
        self.data =  data

    def to_bytestr(self):
        return self.data
    
    @staticmethod
    def from_bytestr(bytestr):
        return PublicKey(bytestr)

    def to_hexstr(self):
        return hexstr(self.data)
    
    @staticmethod
    def from_hexstr(hexstr):
        return PublicKey.from_bytestr(decodehexstr(hexstr))

    def __eq__(self ,other):
        return (self.data == other.data)
        
class Outpoint( object ):
    pass

class PubKeyOutpoint( Outpoint ):
    def __init__(self,  public_key, is_pubkey_hash=True):
        self.public_key =  public_key
        self.is_pubkey_hash = is_pubkey_hash

    def __eq__(self ,other):
        return (self.public_key == other.public_key and
                self.is_pubkey_hash == other.is_pubkey_hash)
        
class MultiSigOutpoint( Outpoint ):
    """ n out of m """
    def __init__(self, n, m, public_key_list):
        self.n = n
        self.m = m
        self.public_key_list = public_key_list
        assert self.m == len(self.public_key_list)
        
    def __eq__(self ,other):
        return (self.n == other.n and
                self.m == other.m and
                self.public_key_list == other.public_key_list)

class ScriptHashOutpoint( object ):
    def __init__(self, script_type, script_length, script):
        self.script_type = script_type
        self.script_length = script_length
        self.script = script
    
class OutpointIndex( object ):
    PUBKEY, PUBKEY_HASH, MULTISIG, SCRIPT_HASH = OUTPOINT_TYPES = range(4)
    """
    Attributes:
        id (int32)
        hash (Uint256)
        index (int32)
        type (enum OutpointIndex.OUTPOINT_TYPES)
        masterkey_id (int32)
        outpoint (instance of PubKeyOutpoint/MultiSigOutpoint/ScriptHashOutpoint)
    """
    def __init__(self, id, hash, index, type, masterkey_id, outpoint):
        self.id = id
        self.hash = hash
        self.index = index
        self.type = type
        self.masterkey_id = masterkey_id
        self.outpoint = outpoint

    def __eq__(self ,other):
        return (self.id == other.id and
                self.hash == other.hash and
                self.index == other.index and
                self.type == other.type and
                self.masterkey_id == other.masterkey_id and
                self.outpoint == other.outpoint)

class Change(object):
    pass

class Delete(Change):
    def apply(self, dct, key):
        del dct[key]

class Set(Change):
    def __init__(self, value):
        self.value = value
    def apply(self, dct, key):
        dct[key] = self.value


class Transaction():
    """
    set + set => set
    set + delete => delete
    delete + delete => error
    delete + set => set
    """
    def __init__(self):
        self.changes = defaultdict(list)
        
    def delete(self, itemset, key):
        if self.isdeleted(itemset, key):
            raise KeyError()
        self.changes[(itemset, key)].append(Delete())
        
    def set(self, itemset, key, value):
        self.changes[(itemset, key)].append(Set(value))

    def isdeleted(self, itemset, key):
        return self.ischanged(itemset, key) and type(self.lastchange(itemset, key)) is Delete
    
    def lastchange(self, itemset, key):
        return self.changes[(itemset, key)][-1]

    def ischanged(self, itemset, key):
        return ((itemset, key) in self.changes and self.changes[(itemset, key)])
    
    def iterchanges(self):
        for key, changes in self.changes.iteritems():
            for change in changes:
                yield (key, change)
                
    def commit(self):
        for (itemset, key), change  in self.iterchanges():
            itemset.ON_CHANGING.fire(key=key, change=change)
        for (itemset, key), change  in self.iterchanges():
            change.apply(itemset.items_by_key, key)
        for (itemset, key), change  in self.iterchanges():
            itemset.ON_CHANGED.fire(change=change)

    
class ItemSet( object ):
    """
    Events:
        ON_CHANGING:  Fires for every change when a commit is started .
                      An exception can be thrown in the event to notify the 
                      ItemSet that the change cannot be applied 
                      (for example, there could be an error when writing to disk).
        ON_CHANGED:   The item was changed successfully.
    """
    def __init__(self, items_by_key=None):
        self.items_by_key = items_by_key or {}
        self.ON_CHANGING = Event() 
        self.ON_CHANGED = Event()
        self.tx = None
    
    def begin_transaction(self, tx=None):
        self.tx = tx or Transaction()
        return self.tx
    
    def commit_transaction(self):
        """ Commit the transaction. 
        
            If an exception is raised in an ON_CHANGING event, the transaction 
            is not applied"""
        self.tx.commit()

    def delete(self, key, tx=None):
        tx = tx or self.tx
        if not tx.ischanged(self, key) and key not in self.items_by_key:
            raise KeyError()
        tx.delete(self, key)
        
    def set(self, key, value, tx=None):
        tx = tx or self.tx
        assert tx != None
        tx.set(self, key, value)
        
    def get(self, key):
        return self.items_by_key[key]

    def contains(self, key):
        return key in self.items_by_key


class BtcWallet(object):
    """
    Attributes:
        masterkeys (ItemSet):
        private_keys (ItemSet):
        outpoints (ItemSet):
    """
    def __init__(self, masterkeys=None, 
                       private_keys=None, 
                       outpoints=None):
        self.masterkeys = masterkeys or ItemSet()
        self.private_keys = private_keys or ItemSet()
        self.outpoints = outpoints or ItemSet()
        self.ON_STARTING_TX = Event()
        self.ON_ENDING_TX = Event()
        
    def begin_transaction(self):
        self.ON_STARTING_TX.fire()
        self.tx = Transaction()
        self.private_keys.begin_transaction(self.tx)
        self.outpoints.begin_transaction(self.tx)
    
    def commit_transaction(self):
        self.ON_ENDING_TX.fire()
        self.tx.commit()




