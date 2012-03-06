# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from logging import Handler, DEBUG, INFO, WARNING, ERROR
from collections import deque
import wx
from wx.richtext import RichTextRange

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
        self.isprocessing = False
        
    def emit(self, record):
        self.records.append(record)
        if not self.isprocessing:
            wx.CallAfter(self.process_logs)
        
    def process_logs(self):
        if len(self.records) > 0:
            record = self.records.pop()
            
            message = self.format(record)
            self.richtext.Freeze()
            self.richtext.BeginSuppressUndo()
            if (self.richtext.GetNumberOfLines() > 5000):
                #self.richtext.MoveHome()
                self.richtext.Remove(0, self.richtext.GetLineLength(0)+1)
                #endfirstline = self.richtext.GetLineLength(0)
                #self.richtext.Replace(0,endfirstline-1, "x-a")
            self.richtext.MoveEnd()
            self.richtext.BeginTextColour(self.LOG_STYLES[record.levelno])
            self.richtext.WriteText(message)
            self.richtext.EndTextColour()
            self.richtext.Newline()
            self.richtext.ShowPosition(self.richtext.GetLastPosition())
            self.richtext.EndSuppressUndo()
            self.richtext.Thaw()
        if len(self.records):
            wx.CallAfter(self.process_logs)
        else:
            self.isprocessing = False
            
