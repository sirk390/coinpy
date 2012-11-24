from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.database.blockchain.objects.disktxpos import DiskTxPos

class DiskTxPosSerializer():
    DISKTXPOS = Structure([Field("<I", "file"),
                           Field("<I", "blockpos"),
                           Field("<I", "txpos")], "disktxpos")

    def serialize(self, disktxpos_obj):
        return (self.DISKTXPOS.serialize([disktxpos_obj.file,
                                          disktxpos_obj.blockpos,
                                          disktxpos_obj.txpos]))

    def deserialize(self, data, cursor=0):
        (file, nblockpos, ntxpos), cursor = self.DISKTXPOS.deserialize(data, cursor)
        return (DiskTxPos(file, nblockpos, ntxpos), cursor)
