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
    def __init__(self, logpanel):
        Handler.__init__(self)
        self.logpanel = logpanel
        self.richtext = self.logpanel.richtext
        self.records = deque()
        
    def emit(self, record):
        self.records.append(record)
        wx.CallAfter(self.process_logs)
        
    def process_logs(self):
        while len(self.records) > 0:
            record = self.records.pop()
            
            message = self.format(record)
            self.richtext.Freeze()
            self.richtext.BeginSuppressUndo()
            self.richtext.MoveEnd()
            self.richtext.BeginTextColour(self.LOG_STYLES[record.levelno])
            self.richtext.WriteText(message)
            self.richtext.EndTextColour()
            self.richtext.Newline()
            self.richtext.ShowPosition(self.richtext.GetLastPosition())
            self.richtext.EndSuppressUndo()
            self.richtext.Thaw()

