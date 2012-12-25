
class MockTimeSource():
    def __init__(self, time):
        self.time = time
    
    def get_time(self):
        return self.time
    