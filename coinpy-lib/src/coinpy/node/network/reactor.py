# -*- coding:utf-8 -*-
"""
Created on 9 Dec 2011

@author: kris
"""
import asyncore
import collections
import time
import heapq
import threading

class Reactor():
    def __init__(self, log):
        self.terminate = False
        self.log = log
        
        self.workqueue = collections.deque()
        self.scheduled_workqueue = [] # priority queue [ time_next_call, (fn, args, kwargs)) ]
        self.scheduled_tasks = {}     # { (fn, args, kwargs) => seconds }
        self.thread = threading.Thread(target=self._run)
        
    def call(self, fn, *args):
        item = (fn, args)
        self.workqueue.append(item)
        
    def schedule_each(self, seconds, fn, *args):
        t = time.time()
        item = (fn, args)
        self.scheduled_tasks[item] = seconds
        heapq.heappush(self.scheduled_workqueue, (t + seconds, item)) 
        #self.log.info("scheduled notify_newhashes")
        
    def _run(self):
        while not self.terminate:
            asyncore.loop(timeout=1, count=1)
            while (len(self.workqueue) > 0):
                fn, args = self.workqueue.popleft()
                fn(*args)
            t = time.time()
            #self.log.info("next schedule : %f, now : %f" % (self.scheduled_workqueue[0][0], t))
            while (self.scheduled_workqueue[0][0] <= t):
                (_, item) = heapq.heappop(self.scheduled_workqueue)
                fn, args = item
                fn(*args)
                heapq.heappush(self.scheduled_workqueue, (t + self.scheduled_tasks[item], item)) 
    
    def start(self):
        self.thread.start()
    def stop(self):
        self.terminate = True
        self.thread.join()
