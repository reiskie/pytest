#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import sys
import datetime


class MyClient(Protocol):
    def __init__(self):
        self.server=None

    def connectionMade(self):
        print("MyClient:Connected to the db2 server!")

    def dataReceived(self, data):
        print("MyClient:dataRecv, got message from db2: ", data)

        if self.transport.connected:
            self.server.transport.write(data)

    def connectionLost(self, reason):
        print("MyClient:Disconnected from the server!")

    def setServer(self,svr):
        self.server=svr


class MyClientFactory(ClientFactory):
    def __init__(self, client):
        self.protocol = client 

    def startedConnecting(self, connector):
        print('MyClientFactory:Started to connect.')

    def buildProtocol(self, addr):
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print('MyClientFactory:Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('MyClientFactory:Connection failed. Reason:', reason)



class MyServer(Protocol):
    def __init__(self):
        self.client=None

    def connectionMade(self):
        print("MyServer:New connection made: %d" % 1)

    def connectionLost(self, reason):
        print("MyServer:Lost connect: %d" % 1)

    def dataReceived(self, data):
        print("MyServer:dataReceived() entered!")
        if data == "close":
            self.transport.loseConnection()
            #self.client.transport.loseConnection()
            print("%s closed" % 1)
        else:
            print("MyServer:Send data to db2 server: %s" % (data))
            #self.client.transport.write(data)
        print("MyServer:dataReceived() exited!")

    def setClient(self,clt):
        self.client=clt


class MyServerFactory(Factory):
    def __init__(self,server):
        self.server=server

    def buildProtocol(self, addr):
        return self.server 


client=MyClient();
server=MyServer();
client.setServer(server);
server.setClient(client);

host = "192.168.1.201"
port = 60000
factory = MyClientFactory(client)
reactor.connectTCP(host, port, factory)

endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(MyServerFactory(server))
reactor.run()  

