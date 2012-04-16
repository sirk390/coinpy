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
import sys


def async_run(it, value=None):
    completed = False
    while not completed:
        try:
            asynch_task = it.send(value)
            value = asynch_task.call()
        except StopIteration:
            completed = True
    return value    
    

class Reactor():
    def __init__(self):
        self.terminate = False
        
        self.asynchs = collections.deque() # instances of Asynch
        self.workqueue = collections.deque()
        self.scheduled_workqueue = [] # priority queue [ time_next_call, (fn, args, kwargs)) ]
        self.scheduled_tasks = {}     # { (fn, args, kwargs) => seconds }
        self.thread = threading.Thread(target=self.run)
        
    def call(self, fn, *args):
        item = (fn, args)
        self.workqueue.append(item)
    
    def call_asynch(self, asynch):
        self.asynchs.append(asynch)

    def schedule_each(self, seconds, fn, *args):
        self.schedule(seconds, fn, True, *args)

    def schedule_later(self, seconds, fn, *args):
        self.schedule(seconds, fn, False, *args)
        
    def schedule(self, seconds, fn, repeat, *args):
        t = time.time()
        item = (fn, args)
        self.scheduled_tasks[item] = seconds
        heapq.heappush(self.scheduled_workqueue, (t + seconds, item, repeat)) 
        #self.log.info("scheduled notify_newhashes")
        
    def run(self):
        work_completed = True
        while not self.terminate:
            #process asyncore network loop
            #note: GUI might send an event during the asyncore.loop
            # so timeout is 0.1 even when work_completed
            # to be fixed somehow
            asyncore.loop(timeout=(0.1 if work_completed else 0.001), count=1)
            #process all workqueue items
            while (len(self.workqueue) > 0):
                fn, args = self.workqueue.popleft()
                fn(*args)
            #process asynch tasks during max 200ms
            nbiterate = 0
            start_time = t = time.time()
            while (len(self.asynchs) > 0 and (t <= (start_time + 0.2)) ): 
                task = self.asynchs.popleft()
                task.run()
                if not task.completed:
                    self.asynchs.append(task)
                nbiterate += 1
                if nbiterate % 10 == 0:
                    t = time.time()
            
            #if nbiterate > 1:
            #    print "reactor executed %d asynch tasks" % (nbiterate)
            #print nbiterate
            work_completed = len(self.asynchs) == 0 and len(self.workqueue) == 0
            #process scheduled items
            t = time.time()
            while (self.scheduled_workqueue and self.scheduled_workqueue[0][0] <= t):
                (_, item, repeat) = heapq.heappop(self.scheduled_workqueue)
                fn, args = item
                fn(*args)
                if repeat:
                    heapq.heappush(self.scheduled_workqueue, (t + self.scheduled_tasks[item], item)) 
            
        if self.stopped_callback:
            self.stopped_callback()
        
    def start(self):
        self.thread.start()
        
    def stop(self, on_stopped=None):
        self.terminate = True
        self.stopped_callback = on_stopped

    def join(self):
        self.thread.join()
        
        
if __name__ == '__main__':
    from coinpy.tools.reactor.asynch import Asynch
    def slow_func_0_1(x):
        return x + 1
    def slow_func_0_2(x):
        return x + 1
    def slow_func1(x):
        x = yield slow_func_0_1(x)
        x = yield slow_func_0_2(x)
        yield x
    def slow_func2(x):
        yield x * 2
    def asynch_func1():
        a = yield slow_func1(1)
        b = yield slow_func2(a)
        yield b
    reactor = Reactor()
    a = Asynch(asynch_func1)
    reactor.call_asych(a)
    
    reactor.start()
    while not a.completed():
        time.sleep(0.01)
    print a.return_value
    reactor.stop()
    