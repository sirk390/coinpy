from coinpy.tools.reactor.reactor import Reactor, reactor
from coinpy.tools.reactor.wx_plugin import WxPlugin
import wx

reactor.install(WxPlugin())

frame = wx.Frame(None)
frame.Show()

reactor.run()    
