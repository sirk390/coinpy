from coinpy.model.constants.bitcoin import COIN

class TxOut():
    def __init__(self, value, script):
        self.value = value  
        self.script = script
                  
    def __eq__(self, other):
        return (self.value == other.value and 
                self.script == other.script)
      
    def __str__(self):
        return ("tx_out: value:%s %s" % (self.value * 1.0 / COIN, str(self.script)))
