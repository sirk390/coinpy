from coinpy.tools.bitcoin.sha256 import double_sha256_2_input
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.protocol.structures.uint256 import Uint256

def next_merkle_level(hashes):
    """hashes: list of bytestring hashes ( use Uint256.get_bytestr() )"""
    n = len(hashes)
    result = []
    # if odd number of hashes, dupplicate the last one.
    if n % 2:
        hashes.append(hashes[-1])
        n += 1
    # compute the next level of hashes
    for i in range(n/2):
        result.append(double_sha256_2_input(hashes[i*2], hashes[i*2+1]))
    return (result)

    
def get_merkle_tree(block):
    merkle_tree = []
    merkle_tree.append([hash_tx(tx).get_bytestr() for tx in block.transactions])
    while (len(merkle_tree[-1]) != 1):
        merkle_tree.append(next_merkle_level(merkle_tree[-1]))
    return (merkle_tree)

def get_merkle_branch(block, index_tx):
    """Get the merkle branch of a transaction.
    
    block:    block that contains the transaction
    index_tx: index of the transaction in the block
    
    Return value: [list of Uint256] 
    The first element is a hash of a transaction at the bottom of the merkle tree.  
    The last element is the merkle root.
    
    The algorithm uses XOR 1, to select the opposite element at each level.
    """
    merkle_branch = []
    merkle_tree = get_merkle_tree(block)
    for level in merkle_tree:
        merkle_branch.append(Uint256.from_bytestr(level[min(index_tx^1, len(level)-1)]))
        index_tx = index_tx >> 1
    return (merkle_branch)


def check_merkle_branch(txhash, merkle_branch, index_tx):
    """Return True if the merkle branch is valid for txhash and index_tx.
       
       Attributes:
           txhash(Uint256): Hash of a Transaction
           merkle_branch(list of Uint256): Merkle Branch
           index_tx(int): Index of the transaction in the block.
        
    """
    hash = txhash.get_bytestr()
    index = index_tx
    otherside_branch, merkle_root = merkle_branch[:-1], merkle_branch[-1]
    for otherside in otherside_branch:
        if index & 1:
            hash = double_sha256_2_input(otherside.get_bytestr(), hash)
        else:
            hash = double_sha256_2_input(hash, otherside.get_bytestr())
        index = index >> 1
        print "u", Uint256.from_bytestr(hash)           
    return (Uint256.from_bytestr(hash) == merkle_root)
    

"""
static Uint256 CheckMerkleBranch(uint256 hash, const vector<uint256>& vMerkleBranch, int nIndex)
    {
        if (nIndex == -1)
            return 0;
        foreach(const Uint256& otherside, vMerkleBranch)
        {
            if (nIndex & 1)
                hash = Hash(BEGIN(otherside), END(otherside), BEGIN(hash), END(hash));
            else
                hash = Hash(BEGIN(hash), END(hash), BEGIN(otherside), END(otherside));
            nIndex >>= 1;
        }
        return hash;
    }

"""


def compute_merkle_root(block):
    hashes = [hash_tx(tx).get_bytestr() for tx in block.transactions]
    while (len(hashes) != 1):
        hashes = next_merkle_level(hashes)
    return (Uint256.from_bytestr(hashes[0]))


