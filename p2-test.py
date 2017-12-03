# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebSockets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtNetwork import QHostAddress
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
        message=QJsonDocument.fromJson(message,error)

        if error.error:
            print(
                "Failed to parse text message as JSON object:",
                message,
                "Error is:", error.errorString()
            )
            return
        elif not message.isObject():
            print("Received JSON message that is not an object: ", message)
            return

        self.messageReceived.emit(message.object(), self)

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

import sys

server=QWebSocketServer(
"QWebChannel Standalone Example Server",
    QWebSocketServer.NonSecureMode
)
print("open web socket server start")
if not server.listen(QHostAddress.LocalHost, 12345):
    print("Failed to open web socket server.")
    exit(1)
print("open web socket server success")
clientWrapper=WebSocketClientWrapper(server)
channel=QWebChannel()
clientWrapper.clientConnected.connect(channel.connectTo)

app = QApplication(sys.argv)
app.setApplicationName("美莱")
app.setApplicationVersion("1.0")
app.setApplicationDisplayName("mylike")
webView = QtWebEngineWidgets.QWebEngineView()
#reg start
channel.registerObject("dialog", webView)
#reg end
webView.show()

webView.load(QtCore.QUrl("http://127.0.0.1:9090/MylikeOMS/a/login?webChannelBaseUrl="+server.serverUrl().toString()))
webView.page().printToPdf();
sys.exit(app.exec_())