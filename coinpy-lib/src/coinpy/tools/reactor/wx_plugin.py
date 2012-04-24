# -*- coding:utf-8 -*-
"""
Created on 23 Apr 2012

@author: kris
"""
import wx

class WxPlugin():
    def __init__(self):
        self.app = wx.App(False) 
        self.evtloop = wx.EventLoop() 
        wx.EventLoop.SetActive(self.evtloop) 
        
    def install(self, reactor):
        pass
        
    def run(self):
        #wx.Yield()
        donework = False
        while self.evtloop.Pending():
            self.evtloop.Dispatch()
            donework = True
        self.app.ProcessIdle()
        return False
   