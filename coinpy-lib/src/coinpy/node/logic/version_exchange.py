from coinpy.model.protocol.services import SERVICES_NONE
from coinpy.model.protocol.messages.types import MSG_VERSION, MSG_VERACK,\
    MESSAGE_NAMES
from coinpy.model.protocol.messages.verack import VerackMessage
from coinpy.model.protocol.messages.version import VersionMessage
import time
from coinpy.tools.observer import Observable
from coinpy.node.logic.status.version_status import VersionStatus
from coinpy.model.protocol.structures.netaddr import Netaddr


class VersionExchangeService():
    EVT_VERSION_EXCHANGED = Observable.createevent()
    EVT_MESSAGE = Observable.createevent()
            
    def __init__(self, node, get_blockchain_height, params, log):
        self.node = node
        self.params = params
        self.log = log
        self.get_blockchain_height = get_blockchain_height
        self.version_statuses = {}
        self.version_exchanged_nodes = set()
        #todo: remove usage of node.params and node.addr_me
        self.addr_me = Netaddr(self.params.enabledservices, "192.168.1.1", 78)
        self.node.subscribe(node.EVT_BASIC_MESSAGE, self.on_message)
        self.node.subscribe(node.EVT_CONNECTED, self.__on_connected)
           
    def __on_connected(self, event):
        self.version_statuses[event.handler] = VersionStatus()
        if (event.handler.isoutbound):
            self.send_version(event.handler)
            
    def __on_version(self, event):
        status = self.version_statuses[event.handler]
        status.version_received = True
        status.version_message = event.message
        self.log.debug("received version (%s: %d)" % (str(event.handler), event.message.version))
        self.send_verack(event.handler)
        if (not event.handler.isoutbound):
            self.send_version(event.handler)
        self.check_version_exchanged(event.handler)
        
    def __on_verack(self, event):
        self.log.debug("received verack (%s)" % (str(event.handler)))
        status = self.version_statuses[event.handler]
        #if (not status.sent_version or status.verack_received):
        #    event.source.handle_close()
        #    return
        status.verack_received = True
        self.check_version_exchanged(event.handler)

    def on_message(self, event):
        if (event.message.type == MSG_VERSION):
            self.__on_version(event)
            return
        if (event.message.type == MSG_VERACK):
            self.__on_verack(event)
            return
        if (event.handler not in self.version_exchanged_nodes):
            self.log.warning("peer %s sent message of type %s before message exchanging version" % (str(event.handler), MESSAGE_NAMES[event.message.type]))
            return
        handler, message = event.handler, event.message
        self.node.emit_message(self.EVT_MESSAGE, message=message, handler=handler)
        self.node.emit_message((self.EVT_MESSAGE, message.type), message=message, handler=handler)
       
    def check_version_exchanged(self, handler):
        if self.version_statuses[handler].versions_exchanged():
            self.log.info("Accepted new peer: %s" % (handler))
            self.version_exchanged_nodes.add(handler)
            #todo: replace 'handler' by 'peer'
            self.node.emit_message(self.EVT_VERSION_EXCHANGED, handler=handler, version_message=self.version_statuses[handler].version_message)
          
    def send_version(self, handler):
        version = VersionMessage(version = self.params.version, 
                     services=self.params.enabledservices, 
                     timestamp=time.time(), 
                     addr_me=self.addr_me, 
                     addr_you=Netaddr(SERVICES_NONE, handler.sockaddr.ip, handler.sockaddr.port), 
                     nonce=self.params.nonce, 
                     sub_version_num=self.params.sub_version_num,
                     start_height=self.get_blockchain_height())
        self.log.debug("Sending version(%s): %s" % (handler.sockaddr, version))
        self.version_statuses[handler].version_sent = True
        handler.send_message(version)

    def send_verack(self, handler):
        verack = VerackMessage()
        self.log.debug("Sending verack(%s): %s" % (handler.sockaddr, verack))
        self.version_statuses[handler].verack_sent = True
        handler.send_message(VerackMessage()) 
         
