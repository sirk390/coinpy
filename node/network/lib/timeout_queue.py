# -*- coding:utf-8 -*-
"""
Created on 16 Nov 2011

@author: kris
"""
from coinpy.tools.datastructures.priority_queue import PriorityQueue
import heapq

class TimeoutQueue(PriorityQueue):
    """    
        timeout:    
            remove and return elements until time 'time'
    """
    def add(self, time, element):
        PriorityQueue.add(self, time, element)
        
    def timeout(self, time):
        return (self.pop_smaller_than(time))

if __name__ == '__main__':
    t = TimeoutQueue()
    t.add(1, "a")
    t.add(5, "b")
    t.add(3, "c")
    t.add(2.5, "d")
    t.add(7, "e")
    print t
    print t.timeout(3.1)
    print t
