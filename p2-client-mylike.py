from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebSockets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtNetwork import QHostAddress
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore
from ctypes import *
import ctypes
import os
import json
import socket
import time
import sys

class WebSocketTransport(QWebChannelAbstractTransport):
    def __init__(self, socket, **kwargs):
        super().__init__(socket, **kwargs)

        self._socket=socket
        self._socket.textMessageReceived.connect(self.textMessageReceived)

    def sendMessage(self, message):
        doc=QJsonDocument(message)
        self._socket.sendTextMessage(doc.toJson(QJsonDocument.Compact))

    @pyqtSlot(str)
    def textMessageReceived(self, message):
        error=QJsonParseError()
        print(message)

        # self.messageReceived.emit(message.object(), self)

class WebSocketClientWrapper(QObject):
    clientConnected=pyqtSignal(WebSocketTransport)

    def __init__(self, server, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._server=server
        self._server.newConnection.connect(self.handleNewConnection)

    @pyqtSlot()
    def handleNewConnection(self):
        self.clientConnected.emit(
            WebSocketTransport(self._server.nextPendingConnection())
        )

class Dialog(QDialog):
    sendText=pyqtSignal(str)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        l=QGridLayout(self)
        self.output=QPlainTextEdit(
            self,
            readOnly=True,
            plainText="Initializing WebChannel...")
        l.addWidget(self.output, 0, 0, 1, 2)

        self.input=QLineEdit(self, placeholderText="Message Contents")
        l.addWidget(self.input, 1, 0)

        self.send=QPushButton("Send", self, clicked=self.clicked)
        l.addWidget(self.send, 1, 1)

    def displayMessage(self, message):
        self.output.appendPlainText(message)

    @pyqtSlot(str)
    def receiveText(self, text):
        self.displayMessage("Received message: {}".format(text))

    @pyqtSlot()
    def clicked(self):
        text=self.input.text()
        if not len(text) or text.isspace(): return

        self.sendText.emit(text)
        self.displayMessage("Sent message: {}".format(text))

        self.input.clear()

if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)

    server=QWebSocketServer(
        "QWebChannel Standalone Example Server",
        QWebSocketServer.NonSecureMode
    )
    if not server.listen(QHostAddress.LocalHost, 12345):
        print("Failed to open web socket server.")
        exit(1)

    clientWrapper=WebSocketClientWrapper(server)

    channel=QWebChannel()
    clientWrapper.clientConnected.connect(channel.connectTo)

    dialog=Dialog()

    # url=QUrl.fromLocalFile("./index.html");
    # url.setQuery("webChannelBaseUrl="+server.serverUrl().toString())
    # QDesktopServices.openUrl(url);
    #
    # dialog.displayMessage(
    #     "Initialization complete, opening browser at {}.".format(
    #         url.toDisplayString()
    #     )
    # )
    # dialog.show()
    # dialog.raise_()
    # app = QApplication(sys.argv)

    a.setApplicationName("美莱")
    a.setApplicationVersion("1.0")
    a.setApplicationDisplayName("mylike")
    webView = QtWebEngineWidgets.QWebEngineView()
    # reg start
    channel.registerObject("dialog", webView)
    # reg end
    webView.show()
    # webView.load(QtCore.QUrl("http://localhost:8080/doc/?webChannelBaseUrl=" + server.serverUrl().toString()))
    # webView.load(QtCore.QUrl("D:/mydocument/study/python/pyqt/standalone/index.html?webChannelBaseUrl=" + server.serverUrl().toString()))
    webView.load(QtCore.QUrl("D:/soft/bustools/print/PrintSample47.html?webChannelBaseUrl=" + server.serverUrl().toString()))

    exit(a.exec_())
