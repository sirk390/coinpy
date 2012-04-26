# -*- coding:utf-8 -*-
"""
Created on 9 Dec 2011

@author: kris
"""
import collections
import time
import heapq
import threading

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
        self.thread = threading.Thread(target=self.run)
        self.reset()

    def reset(self):
        self.terminate = False
        self.asynchs = collections.deque() # instances of Asynch
        self.workqueue = collections.deque()
        self.scheduled_workqueue = [] # priority queue [ time_next_call, (fn, args, kwargs)) ]
        self.scheduled_tasks = {}     # { (fn, args, kwargs) => seconds }
        self.plugins = [] 
        self.plugin_types = [] 
             
    def call(self, fn, *args, **kwargs):
        item = (fn, args, kwargs)
        self.workqueue.append(item)
    
    def call_later(self, seconds, fn, *args):
        self.schedule(seconds, fn, False, *args)

    def schedule_each(self, seconds, fn, *args):
        self.schedule(seconds, fn, True, *args)

    def schedule(self, seconds, fn, repeat, *args):
        t = time.time()
        item = (fn, args)
        self.scheduled_tasks[item] = seconds
        heapq.heappush(self.scheduled_workqueue, (t + seconds, item, repeat)) 
        #self.log.info("scheduled notify_newhashes")
    
    def install(self, plugin):
        if type(plugin) not in self.plugin_types:
            plugin.install(self)
            self.plugins.append(plugin)
            self.plugin_types.append(type(plugin))
            
    def run(self):
        while not self.terminate:  #50ms per loop (latency for new incoming events)
            # run plugins
            working = True
            t = time.time()
            isactive = [True for p in self.plugins]
            haswork = False
            while working:  #max 50ms
                for i, p in enumerate(self.plugins):
                    if isactive[i]:
                        isactive[i] = p.run()
                # process workqueue items
                if self.workqueue:
                    fn, args, kwargs = self.workqueue.popleft()
                    r = fn(*args, **kwargs)
                didwork = any(isactive)
                haswork = haswork or didwork or self.workqueue
                working = didwork and (time.time() < t + 0.05)                
            #process scheduled items (latency 50ms)
            t = time.time()
            while (self.scheduled_workqueue and self.scheduled_workqueue[0][0] <= t):
                (_, item, repeat) = heapq.heappop(self.scheduled_workqueue)
                fn, args = item
                fn(*args)
                if repeat:
                    heapq.heappush(self.scheduled_workqueue, (t + self.scheduled_tasks[item], item)) 
            if not haswork:
                time.sleep(0.05)
                
        if self.stopped_callback:
            self.stopped_callback()
        
    def start(self):
        self.thread.start()
        
    def stop(self, on_stopped=None):
        self.terminate = True
        self.stopped_callback = on_stopped

    def join(self):
        self.thread.join()
        
reactor = Reactor()
   
if __name__ == '__main__':
    pass