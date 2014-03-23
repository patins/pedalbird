from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource
from twisted.web.server import Site
from twisted.web.static import File
from twisted.protocols import basic
from twisted.internet.serialport import SerialPort

class BroadcastServerProtocol(WebSocketServerProtocol):
   def onOpen(self):
      self.factory.register(self)

   def connectionLost(self, reason):
      WebSocketServerProtocol.connectionLost(self, reason)
      self.factory.unregister(self)

class BroadcastServerFactory(WebSocketServerFactory):
   def __init__(self, url, debug = False, debugCodePaths = False):
      WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
      self.clients = []

   def register(self, client):
      if not client in self.clients:
         self.clients.append(client)

   def unregister(self, client):
      if client in self.clients:
         self.clients.remove(client)

   def broadcast(self, msg):
      for c in self.clients:
         c.sendMessage(msg.encode('utf8'))

class ArduinoClient(basic.LineReceiver):
    def lineReceived(self, line):
        self.broadcast_server.broadcast(line)

if __name__ == "__main__":
    port = 8080
    factory = BroadcastServerFactory("ws://localhost:" + str(port))
    factory.protocol = BroadcastServerProtocol
    resource = WebSocketResource(factory)
    root = File("game/")
    root.putChild('pedal', resource)
    site = Site(root)
    reactor.listenTCP(port, site)
    arduino_client = ArduinoClient()
    arduino_client.broadcast_server = factory
    SerialPort(arduino_client, 'COM3', reactor, baudrate='9600')
    reactor.run()