import StringIO

class IoHandle( object ):
    def __init__(self, iohandle, size):
        self.iohandle = iohandle
        self.size = size
        
    def write(self, offset, data):
        print "write", offset, data
        self.iohandle.seek(offset)
        return self.iohandle.write(data)
        
    def read(self, offset, length):
        self.iohandle.seek(offset)
        return self.iohandle.read(length)
    
    @classmethod
    def from_string(cls, s):
        return cls(StringIO.StringIO(s), len(s))

    @classmethod
    def using_stringio(cls, size):
        return cls(StringIO.StringIO("\x00" * size), size)

class IoSectionHandle( object ):
    """ Read or Write to a subsection of a file """
    def __init__(self, random_access_iohandle, section_offset, length):
        self.random_access_iohandle = random_access_iohandle
        self.section_offset = section_offset
        self.length = length
        
    def write(self, offset, data):
        if len(data) > self.length:
            raise Exception("unable to write: data too long")
        return self.random_access_handle.write(self.section_offset + offset, data)
        
    def read(self, offset, length):
        if offset + length < self.length:
            raise Exception("unable to read: not enough data")
        return self.random_access_handle.read(self.section_offset + offset, length)

