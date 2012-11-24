import random

class IdPool():
    def __init__(self, min=0, max=10000):
        self.allocated_ids = set()
        self.min = min
        self.max = max
        self.maxallocated = (max - min) * 0.8
        
    def get_id(self):
        if len(self.allocated_ids) > self.maxallocated:
            raise Exception("get_id: Not enough ids.")
        id = random.randint(self.min, self.max)
        while id in self.allocated_ids:
            id = random.randint(self.min, self.max)
        self.allocated_ids.add(id)
        return id
            
    def release_id(self, id):
        if id not in self.allocated_ids:
            raise Exception("release_id: id:%d is not allocated" % (id))
        self.allocated_ids.remove(id)

        