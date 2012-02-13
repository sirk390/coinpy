# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from logging import Handler, DEBUG, INFO, WARNING, ERROR
from collections import deque
import wx

class GuiLogHandler(Handler):
    LOG_STYLES = { DEBUG  : (0, 0, 255),
                   INFO  : (0, 0, 0),
                   WARNING : (255, 128, 0),
                   ERROR  : (255, 0, 0)}
    def __init__(self, richtextctrl):
        Handler.__init__(self)
        self.richtextctrl = richtextctrl
        self.records = deque()
        
    def emit(self, record):
        self.records.append(record)
        wx.CallAfter(self.process_logs)
        
    def process_logs(self):
        while len(self.records) > 0:
            record = self.records.pop()
            
            message = record.getMessage()
            self.richtextctrl.Freeze()
            self.richtextctrl.BeginSuppressUndo()
            self.richtextctrl.MoveEnd()
            self.richtextctrl.BeginTextColour(self.LOG_STYLES[record.levelno])
            self.richtextctrl.WriteText( message)
            self.richtextctrl.EndTextColour()
            self.richtextctrl.Newline()
            self.richtextctrl.ShowPosition(self.richtextctrl.GetLastPosition())
            self.richtextctrl.EndSuppressUndo()
            self.richtextctrl.Thaw()

