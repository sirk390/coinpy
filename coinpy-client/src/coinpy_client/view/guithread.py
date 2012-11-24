import wx

def guithread(fct):
    #def run_with_callback(fct, args, callback=None):
    #    fct(*args)
    #    if callback:
    #        callback()
    def runner(*args):
        wx.CallAfter(fct, *args)
    return runner
