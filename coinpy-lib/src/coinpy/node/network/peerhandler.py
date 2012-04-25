import asyncore
import socket
import traceback
from coinpy.tools.observer import Observable

"""
Note: We are not using dispatcher_with_send as it doesn't take into account 
writability before sending data (bug of calling initiate_send() in dispatcher_with_send.send() ?)
This very small feature is reimplemented here.
"""
class PeerHandler(asyncore.dispatcher, Observable):
    EVT_CONNECT = Observable.createevent()
    EVT_DISCONNECT = Observable.createevent()
   
    def __init__(self, sockaddr, sock=None):
        Observable.__init__(self)
        asyncore.dispatcher.__init__(self, sock=sock)
        self.sockaddr = sockaddr
        self.isoutbound = (sock == None)
        self.out_buffer = ""
        if not sock:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((sockaddr.ip, sockaddr.port))
                
    def handle_connect(self):
        self.fire(self.EVT_CONNECT)
 
    def handle_error(self):
        traceback.print_exc()
            
    def handle_close(self):
        self.fire(self.EVT_DISCONNECT)
        self.close()

    def writable(self):
        return (not self.connected) or len(self.out_buffer)

    def handle_write(self):
        num_sent = asyncore.dispatcher.send(self, self.out_buffer[:512])
        self.out_buffer = self.out_buffer[num_sent:]
               
    def send(self, data):
        self.out_buffer = self.out_buffer + data

    def __str__(self):
        return str(self.sockaddr)
