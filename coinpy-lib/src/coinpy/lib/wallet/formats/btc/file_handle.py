import StringIO

class IoHandle( object ):
    def __init__(self, iohandle, debug=False):
        self.iohandle = iohandle
        #sel.size = size
        self.debug = debug
    
    def write(self, offset=None, data=""):
        if self.debug:
            print "write", offset, repr(data)
        if offset is not None:
            self.iohandle.seek(offset)
        return self.iohandle.write(data)
        
    def read(self, offset=None, length=0):
        if offset is not None:
            self.iohandle.seek(offset)
        return self.iohandle.read(length)

    def seek(self, offset, whence):
        self.iohandle.seek(offset, whence)

    def tell(self):
        return self.iohandle.tell()
    
    @classmethod
    def from_string(cls, s):
        return cls(StringIO.StringIO(s))

    @classmethod
    def using_stringio(cls, size=0):
        return cls(StringIO.StringIO("\x00" * size))

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

