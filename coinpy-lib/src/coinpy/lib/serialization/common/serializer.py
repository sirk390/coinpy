
class Serializer(object):
    def __init__(self, desc=""):
        self.desc = desc
    def serialize(self, value):
        pass
    def deserialize(self, data, cursor):
        return ("", cursor)
    def get_size(self):
        pass 