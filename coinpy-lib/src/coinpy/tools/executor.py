import collections

class Executor():
    """Basic Synchroneous executor"""
    def __init__(self):
        self.workqueue = collections.deque()
        
    def submit(self, fn, *args, **kwargs):
        self.workqueue.append((fn, args, kwargs))

    def execute(self, count=10):
        while (self.workqueue.size() > 0 and count > 0):
            fn, args, kwargs = self.workqueue.popleft()
            result = fn(*args, **kwargs)
            count -= 1
