* Header
* Chunks
* Standard Chunks
  * bLOG (wal buffer)
  * ILOG (wal index)
  * mKEY (masterkeys)
  * pKEY (keys)
  * tOUT (outpoints)
  * eMPT (empty)
* Encryption
* Atomicity & Durability
  * writing
  * startup & recovery

*******************
Header
*******************
A WLT file starts with the hexadeciaml 12-byte header consisting of a signature and a version number.

+----------------+-----------------+
| Field          | Size            |
+================+=================+
| signature      | 8bytes          |  89 57 4C 54 0D 0A 1A 0A
+----------------+-----------------+
| version        | 4bytes          |  Big endian integer. Chunk format version.
|                |                 |  Only the value 1 is allowed.
+----------------+-----------------+

After the header follows a list of chunks.

*******************
Chunks
*******************
Inspired by IFF/RIFF/PNG, chunks have a similar format with a 8 byte chunk_id.

+----------------+-----------------+
| Field          | Size            |
+================+=================+
| chunk_id       | 4bytes          |  Standard values: ILOG, bLOG, mKEY, sKEY, pOUT
+----------------+-----------------+
| version        | 4bytes          |  big endian integer. See chunk types.
+----------------+-----------------+
| length         | 4bytes          | 
+----------------+-----------------+
| crc            | 4bytes          |
+----------------+-----------------+
| data           | length bytes    |
+----------------+-----------------+

*******************
Standard Chunks
*******************
 
  * ILOG (log index)
  * bLOG (log buffer)
  * mKEY (masterkeys)
  * sKEY (keys)
  * pOUT (outpoints)
  * iNFO (wallet metadata)
  * aCNT (Accounts)
  * uTXS (Unsubmitted or Unsigned Transaction)

Not all programs needs to read or handle every chunk, however every program should at least scan the wal_index.
By verifying that there is no uncommitted modification, a program will make sure the wallet is in a coherent state.

=============
wal
=============

The wal chunk is a buffer for write ahead log entries.
It contains write entries of the following format:

+----------------+-----------------+
| Field          | Size            |
+================+=================+
| write_address  | 4bytes          | 
+----------------+-----------------+
| write_length   | 4bytes          | 
+----------------+-----------------+
| data           | length bytes    |
+----------------+-----------------+
| original_data  | length bytes    |
+----------------+-----------------+

The entries can be located anywhere in the chunk. 
The wal_index chunk needs to be used to locate them.

=============
wal_index
=============
This is the only critical chunk. It contains a list of uncommitted changes.

It consists in a list of 6 byte entries filling the complete chunk (There are chunk_size / 6 entries):

+----------------+-----------------+
| Field          | Size            |
+================+=================+
| command        | 1byte           | 1:begin_transaction, 2:end_transaction, 3:write. 4:change_file_size 
+----------------+-----------------+
| argument       | 4bytes          | write: relative address in the "wal data". 
|                |                 | begin_transaction;0, end_transaction: 0
|                |                 | change_file_size: new_size
+----------------+-----------------+
| needs_commit   | 1byte           | 1 (big endian) if still needs to be committed, 0 otherwise 
+----------------+-----------------+

Every decoders needs at least to verify at startup there are no "needs_commit" fields equals to 1.

=================
masterkeys (mKEY)
=================

+----------------+------------------+
| Field          | Size             |
+================+==================+
| count          | 4bytes           |
+----------------+------------------+
| master_keys    | count*128        |
+----------------+------------------+

Master Keys:
+-----------------+------------------+
| Field           | Size             |
+=================+==================+
| id              | 4bytes           |  master key id (referenced in keys and outpoints)
+-----------------+------------------+
| crypted_key     | 32bytes          |  Encrypted Master Key
+-----------------+------------------+
| salt            | 8bytes           |  Encryption Salt
+-----------------+------------------+
| deriv_method    | 1byte            |  Derivation method, 0:EVP_sha512, 1:scrypt
+-----------------+------------------+
| deriv_iterations| 4bytes           |  Derivation iteration count
+-----------------+------------------+

===================
private keys (pKEY)
===================
List of private keys. 
They are identified by an id unique in the outpoints. 
In case a key is removed, the last entry in the list takes its place and the last entry is erased.

An id uniquely identifies a key in the wallet and at a particular point in time (id's can be re-used).

+----------------+------------------+
| Field          | Size             |
+================+==================+
| count          | 4bytes           |
+----------------+------------------+
| keys           | count*128        |
+----------------+------------------+

Keys:
+-----------------+------------------+
| Field           | Size             |
+=================+==================+
| format          | 8bytes           |  0:std, 1:bip32
+-----------------+------------------+
| id              | 4bytes           |  key id, unique in the wallet (outpoints refer to it)
+-----------------+------------------+
| master_key_id   | 4bytes           |  id of the master key that is used for encryption (-1 if not encrypted).
+-----------------+------------------+
| data_length     | 4bytes           | 
+-----------------+------------------+
| data            | 108 bytes        | 
+-----------------+------------------+

 * std
+----------------+--------------------+
| private_key    | 32bytes            |
+----------------+--------------------+

 * bip32

 
=================
Outpoints (tOUT)
=================

Outpoint metainfo entries consist of the following fields.
In case master_key_id is specified every field is encrypted except data_length and master_key_id.

+--------------------+--------------------+
| outpoint_hash (*)  | 32bytes            |
|                    |                    |
+--------------------+--------------------+
| outpoint_index (*) | 1byte              |
+--------------------+--------------------+
| outpoint_type (*)  | 1byte              | 
+--------------------+--------------------+
| master_key_id      | 4bytes             |  id of the master key that is used for encryption (-1 if not encrypted).
+--------------------+--------------------+
| data_length        | 4bytes             |
+--------------------+--------------------+
| data (*)           | data_length bytes  |
+--------------------+--------------------+
(*) Encrypted if master_key_id is different of -1.
 
Outpoint types:
	1. PUBKEY
	2. PUBKEYHASH
	3. MULTISIG 
	4. SCRIPTHASH

PUBKEY, PUBKEYHASH
------------------
The data contains 33 bytes compressed public_key. data_length is 33 (the first is 0x02 or 0x03). 
See sec1-v2.pdf section 2.3.4 (compressed key). 

SCRIPTHASH
-----------------
pay-to-script-hash // e.g. OP_HASH160 20 [20 byte hash] OP_EQUAL

MULTISIG
-----------------
The data contains N*33 bytes of public_key. data_length is N*33. 
See sec1-v2.pdf section 2.3.4 (compressed key).


=================
Empty (eMPT)
=================
Empty chunks are chunks that contain no data (usually initialized to 0 to make sure the previous information is erased). 
If large enough, they can be used to create a new chunk.

**********************
Encryption
**********************
The following entries support encryptions:
  * Private keys (pKEY)
  * Outpoints (tOUT)
They reference a master_key_id that should be used for encryption.

As in Qt-Bitcoin, fields are encrypted using AES256 and one of the following key derivation algorithms:
  * EVP_sha512
  * scrypt 

**********************
Atomicity & Durability
**********************

=============
Writing
=============

  - Before any writing, the software should make sure that the file is in a known state.
	  - The entries in wal_index must have "uncommitted" set to 0. 
	  
  - 

=============
Startup
=============
	  - Read the wal_index, and verify that all "uncommitted" are set to 0. If they are all 0 the 
	  startup is completed, otherwise a recovery needs to be done:

Recovery:	  
	- wal_index may be in the following state:
		Starts with zero or more "uncommitted" entries set to 0's continue with entries with "uncommitted"  set to 1, the again zero or more entries with "uncommitted" set to 0. 
	In any other state the recovery cannot be completed.
	
	If a transaction at the end is starting with uncommitted=1 and ending with uncommitted's=0 the wal_index
		was not written completly. This last transactions is incomplete, and as it wasn't yet 
		committed to disk, 	the software may erase the entries in the wal_index starting from 
		the end (in case it fails again).
		
	Every entry with "uncommitted" set to 1, can now be applied to disk, from the beginning to the end. After each applied entry set the "uncommitted" byte to 0.
	
	
*******************
Use cases
*******************
Recovery:
	- Crash during commit to disk of wal_index (e.g. some entries at the beginning are applied, one is partially applied, and the end ones are not applied at all)
	- Crash while appending some entries to the wal_index.
	
High level:	
	- Bitcoin client (multiwallet)
	- Wallet agents (controlled remotely)
	- Wallet read app (display, export, convert, stealer)
	- Wallet write app (fix, upgrade)
	- Backed-up wallet

Encryption:	
	- Encrypt private keys.
	- Encrypt Outpoint + public key
	
Modify/Fix wallet:
	- Add a missing outpoint metainfo entry.
	- Add a missing key.
	
=============
# secp256k1
_p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
_r  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
_b  = 0x0000000000000000000000000000000000000000000000000000000000000007L
_a  = 0x0000000000000000000000000000000000000000000000000000000000000000L
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L

curve_secp256k1 = ecdsa.ellipticcurve.CurveFp (_p, _a, _b)
generator_secp256k1 = g = ecdsa.ellipticcurve.Point (curve_secp256k1, _Gx, _Gy, _r)
randrange = random.SystemRandom().randrange
secp256k1 = ecdsa.curves.Curve (
    "secp256k1",
    curve_secp256k1,
    generator_secp256k1,
    (1, 3, 132, 0, 10)
    )
# add this to the list of official NIST curves.
ecdsa.curves.curves.append (secp256k1)


=============