from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.common.field import Field
from coinpy.model.wallet.masterkey import MasterKey

class MasterKeySerializer():
    MASTER_KEY = Structure([VarstrSerializer(),
                            VarstrSerializer(),
                            Field("<I"),
                            Field("<I"),
                            VarstrSerializer()])
    
    def serialize(self, master_key):
        return (self.MASTER_KEY.serialize([master_key.crypted_key,
                                           master_key.salt,
                                           master_key.derivation_method,
                                           master_key.derive_iterations,
                                           master_key.other_derivation_parameters]))

    def deserialize(self, data, cursor):
        master_key_fields, cursor = self.MASTER_KEY.deserialize(data, cursor)
        (crypted_key, salt, derivation_method, derive_iterations, other_derivation_parameters) = master_key_fields
        return (MasterKey(crypted_key, salt, derivation_method, derive_iterations, other_derivation_parameters), cursor)

if __name__ == '__main__':
    from coinpy.tools.hex import decodehexstr
    
    masterkey_bin = decodehexstr("30be4afa6923ad06790b0f8c3345131499cf2b149ca422bd11a7e67a76347c51a456a2d626f75da1ff809632fca7165d71088cdcbd8a494b0eeb0000000089b0000000")
    s = MasterKeySerializer()
    master_key, cursor = s.deserialize(masterkey_bin, 0)
    print master_key
    data = s.serialize(master_key)
    assert data == masterkey_bin
