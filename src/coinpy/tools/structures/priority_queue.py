# -*- coding:utf-8 -*-
"""
Created on 16 Nov 2011

@author: kris
"""
import heapq
import collections

class PriorityQueue():
    Item = collections.namedtuple("Item", "priority removed elm")
        
    def __init__(self):
        self.queue = []
        self.itemdict = {}
    
    def add(self, priority, elm):
        if (elm in self.itemdict):
            raise Exception("Item allready present" )
        item = self.Item(priority, False, elm)
        heapq.heappush(self.queue, item)
        self.itemdict[elm] = item


    
    def remove(self, elm):
        if (elm not in self.itemdict):
            raise KeyError("PriorityQueue: element %s not found" % str(elm))
        if (elm == min(self.queue).elm):
            heapq.heappop(self.queue)
        else:
            self.itemdict[elm].removed = True
        del self.itemdict[elm]
                   
    def __contains__(self, elm):
        return ((elm in self.itemdict) and (not self.itemdict[elm].removed))

    def __len__(self):
        return (len(self.itemdict))

    def peek(self):
        if (len(self) == 0):
            raise KeyError("PriorityQueue : empty")
        while (len(self) > 0 and (self.queue[0].removed)):
            heapq.heappop(self.queue)
        return (self.queue[0].priority, self.queue[0].elm)

    def pop(self):
        priority, item = self.peek()
        self.remove(item)
        return (priority, item)

    def __str__(self):
        return str(",".join(["(%d,%s)" % (i.priority, str(i.elm)) for i in sorted(self.queue) if not i.removed]))

    def pop_smaller_than(self, priority):
        result = []
        while (len(self) > 0 and self.peek()[0] < priority):
            result.append(self.pop())
        return (result)


