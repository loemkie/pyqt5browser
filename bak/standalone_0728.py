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
import google.protobuf
import msg_pb2
import time
import sys
import traceback;
import threading;
from ini_op import Config;
from log_util import LogUtil;
from printer import Printer;
from PyQt5.QtNetwork import *;
#ini 文件
from PyQt5.QtPrintSupport import QPrinter;
import urllib.request;
log=LogUtil();
config = Config("config.ini")
port = 9999;#端口
# host = 'localhost';#OM server
host=config.get("baseconf", "oms_host")
BUFSIZE=8192

#设置连接超时 要保证客户的接收文件服务器不能断
#录音文件的接收器和应用服务器同一台，不会断
# socket.setdefaulttimeout(0.01)
#连接OM server

class OMClient(threading.Thread):
    def reconnect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
            self.client.connect((host, port))
            log.info("重新连接OM Server 成功")
        except:
            log.info("重新连接OM Server 失败")
    def __init__(self,threadname):
        threading.Thread.__init__(self, name=threadname)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
        isSuccess = False;
        try:
            self.client.connect((host, port))
            isSuccess=True;
        except:
            # info = sys.exc_info()
            # print(info[0], ":", info[1], ":", info[2])
            # traceback.print_tb(info[2], limit=1, file=sys.stdout)
            log.info(" 初始化连接 OM server 失败!")
            # print("初始化连接 OM server 失败!")
        if isSuccess==True:
            log.info("连接 OM server 成功!")
            # print("连接 OM server 成功!")

    def run(self):
        while True:
            log.info("监听OM消息开始..端口:"+str(port))
            try:
                data = self.client.recv(BUFSIZE)
                if not data:
                    break;
                self.parseMsgFromOmServer(data);
            except:
                info = sys.exc_info()
                print(info[0], ":", info[1], ":", info[2])
                traceback.print_tb(info[2], limit=1, file=sys.stdout)
                log.info("从OM Server接收消息 失败");
                # print("从OM Server接收消息 失败");
                log.info(config.get("baseconf", "timeout")+"s 后重新连接");
                time.sleep(int(config.get("baseconf", "timeout")))
                omClient.reconnect()
                # break;
    # 外呼
    def send(self,outerTo,extId):
        try:
            # outerTo="";#外呼号码
            # extId="";#分机号
            xmlData="<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<Transfer attribute=\"Connect\">\n<outer to=\""+outerTo+"\"/>\n<ext id=\""+extId+"\"/>\n</Transfer>";
            # xmlData="15980882896"
            #xmlData.encode();
            msg=msg_pb2.Msg();
            msg.id="1";
            msg.cmd=xmlData;
            # self.client.sendall(msg.SerializeToString())
            self.client.sendall(msg.SerializeToString())
            # print('send data ' + xmlData)
            log.info('send data ' + xmlData)
            #time.sleep(1)  # 如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点
            # data = self.client.recv(BUFSIZE)
            # self.parseProtobufMsg(data);
        except:
            info = sys.exc_info()
            # print(info[0], ":", info[1], ":", info[2])
            # traceback.print_tb(info[2], limit=1, file=sys.stdout)
            # print("发送消息至 OM Server失败")
            log.info("连接OM Server失败")
    def parseProtobufMsg(self,data):
        rsp = msg_pb2.Msg();
        rspMsg = rsp.ParseFromString(data);
        log.info("收到服务端应答：");
        log.info(rsp)
        webView.page().runJavaScript("alertIncoming('" + rsp.cmd + "')")
    def parseMsgFromOmServer(self,data):
        # msg=str(data)
        # print(msg);
        self.parseProtobufMsg(data);
    def recv(self, buff=BUFSIZE):
        reply= self.client.recv(buff)
        return  reply;
    def __del__(self):
        self.client.close()

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False
        self.client.close()

class WebSocketTransport(QWebChannelAbstractTransport):


    def __init__(self, socket, **kwargs):
        super().__init__(socket, **kwargs)

        self._socket = socket
        self._socket.textMessageReceived.connect(self.textMessageReceived);

    def sendMessage(self, message):
        doc = QJsonDocument(message)
        # byte_array = QByteArray();
        # byte_array.append(doc.toJson(QJsonDocument.Compact))
        # self._socket.sendTextMessage(byte_array)
        result = doc.toVariant();
        # print(result["type"])
        # log.info("type:"+str(result["type"]))
        if result["type"] == 4.0:#拨号
            # str="{type:10,id:"+str(int(result["id"]))+"}"
            # self._socket.sendTextMessage(str);
            try:
                if "id" in result.keys():
                    id=result["id"]
                    self._socket.sendTextMessage("{\"type\":10,\"id\":"+str(id)+"}")# 类型需要转换为字符串
                    # 调用js
                    # tel = "15980882896";
                    # webView.page().runJavaScript("alert(git.getValue);alertx('发送拨号命令成功 to:" + result["outerTo"] + "')")
                    webView.page().runJavaScript("alertIncoming('"+result["outerTo"]+"')")
                    omClient.send(result["outerTo"],result["extId"]);
                else:
                    # print("no id property in result")
                    log.info("sendMessage no id property in result")
            except:
                info = sys.exc_info()
                log.error(info[0], ":", info[1], ":", info[2])
                traceback.print_tb(info[2], limit=1, file=sys.stdout)
                try:
                    omClient.client.close();
                    omClient.reconnect();
                    log.info("重新连接服务端成功");
                    log.info("重新发送报文");
                    omClient.send(result["outerTo"], result["extId"]);
                except:
                    info = sys.exc_info()
                    log.error(info[0], ":", info[1], ":", info[2])
                    traceback.print_tb(info[2], limit=1, file=sys.stdout)
            # try:
            #     dll = ctypes.windll.LoadLibrary(os.getcwd()+"\\dll\\Termb.dll")
            #     dll.CVR_InitComm(1001)
            #     dll.CVR_Authenticate()
            #     dll.CVR_Read_Content()
            #     webView.page().runJavaScript("receiveDia('" + dll.GetPeopleName() + "')")
            # finally:
            #     webView.page().runJavaScript("receiveDia('读卡失败')")
        if result["type"] == 11:#11代表读卡
            self.readCard(result)
        if result["type"] == 12:#12代表下载
            self.download(result)
        if result["type"] == 13:#13代表打印
            self.print(result)
        # print("response success");
        log.info("response success");
        # 读身份证信息
    #打印
    def print(self,msg):
        try:
            myPrinter = Printer();
            htmlText = "";
            htmlText = msg["html"];
            if (htmlText == ""):
                htmlText = "<p>美莱项目组欢迎您!</p>";
            if msg["pageSize"] == 1:
                # myPrinter.printer.setPageSize(QPrinter.A4)
                # myPrinter.printer.setPageMargins(0, 0, 0, 0, QPrinter.Inch)
                # myPrinter.printer.setFullPage(True);
                # myPrinter.printer.setOutputFormat(QPrinter.NativeFormat);
                myPrinter.printReciept(htmlText);
            if msg["pageSize"] == 2:
                myPrinter.printer.setPageSize(QPrinter.A4)
                myPrinter.printViaHtml(htmlText);
            if msg["pageSize"] == 3:
                myPrinter.printer.setPageSize(QPrinter.Letter)
                myPrinter.printViaHtml(htmlText);
            if msg["pageSize"] == 4:
                myPrinter.printer.setPageSize(QPrinter.A2)
                myPrinter.printViaHtml(htmlText);
        except:
            info = sys.exc_info()
            log.error(info[0], ":", info[1], ":", info[2])
            traceback.print_tb(info[2], limit=1, file=sys.stdout)

    #弹出下载文件选择框
    def download(self, msg):
        url = msg["url"];
        title = msg["title"];
        fname = os.path.basename(url)
        extName = fname.split(".")[1];
        filename, ok2 = QFileDialog.getSaveFileName(dialog, title, "C:/"+fname, 'File (*.*)');
        log.info(filename);
        data={};
        data["type"] = 10;
        data["id"] = msg["id"];
        pos = filename.rfind("/")
        if not filename[:pos] =="":
            # //download
            # downloader = Downloader(url, filename)
            # downloader.download()
            # downloader = Downloader("https://www.baidu.com/img/computer_pc_f9e71b7cee2d086842457387be642f5e.gif",'C:/1.gif')
            # downloader.download()
            # os.startfile(filename[:pos]);#打开目录
            # urllib.request.urlretrieve(url,filename)
            self._socket.sendTextMessage(json.dumps(data))
    def readCard(self,msg):
        dll = ctypes.windll.LoadLibrary(os.getcwd() + "/dll/termb.dll")
        userInfo = {};
        for port in range(1001, 1006):
            result = dll.CVR_InitComm(port)
            if result == 1:
                break
        if result==0:
            log.error("读取USB端口失败")
            userInfo["error"] = "读取USB端口失败";
        if dll.CVR_Authenticate() == 1:
            if (dll.CVR_Read_Content(1)) == 1:
                log.info("读卡成功")
                name = create_string_buffer(128)
                sex=create_string_buffer(128)
                nation=create_string_buffer(128)
                birth=create_string_buffer(128)
                address=create_string_buffer(128)
                id=create_string_buffer(128)
                depart=create_string_buffer(128)
                startDate=create_string_buffer(128)
                endDate=create_string_buffer(128)

                # GetPeopleName=dll.GetPeopleName
                # GetPeopleSex=dll.GetPeopleSex
                # GetPeopleName.restype = c_char_p;
                # GetPeopleName.argtypes = [POINTER(c_char), POINTER(c_int)];
                dll.GetPeopleName(name,pointer(c_int(15)))
                dll.GetPeopleSex(sex, pointer(c_int(1)))
                dll.GetPeopleNation(nation, pointer(c_int(2)))
                dll.GetPeopleBirthday(birth, pointer(c_int(8)));
                dll.GetPeopleAddress(address, pointer(c_int(35)));
                dll.GetPeopleIDCode(id, pointer(c_int(18)));
                dll.GetDepartment(depart, pointer(c_int(15)));
                dll.GetStartDate(startDate, pointer(c_int(8)));
                dll.GetEndDate(endDate, pointer(c_int(8)))
                log.info(str(name.value, encoding="gbk")+str(sex.value, encoding="gbk")+str(nation.value, encoding="gbk")
                    +str(birth.value, encoding="gbk")
                    + str(address.value, encoding="gbk")
                    +str(id.value, encoding="gbk")
                    +str(depart.value, encoding="gbk")
                    +str(startDate.value, encoding="gbk")
                    +str(endDate.value, encoding="gbk"))
                userInfo["name"] =str(name.value, encoding="gbk");
                userInfo["sex"]= str(sex.value, encoding="gbk");
                userInfo["nation"]= str(nation.value, encoding="gbk");
                userInfo["birth"]= str(birth.value, encoding="gbk");
                userInfo["address"]= str(address.value, encoding="gbk");
                userInfo["certificateNumber"]= str(id.value, encoding="gbk");
                userInfo["depart"]= str(depart.value, encoding="gbk");
                userInfo["startDate"] =str(startDate.value, encoding="gbk")
                userInfo["endDate"]=str(endDate.value, encoding="gbk");
                # webView.page().runJavaScript("alert('读身份证信息成功')")
        else:
            # print("认证失败")
            log.info("认证失败");
            userInfo["error"]="认证失败，请重放身份证到读卡器上";
        userInfo["id"] = msg["id"];
        userInfo["type"] = 10;
        self._socket.sendTextMessage(json.dumps(userInfo))

    @pyqtSlot(str)
    def textMessageReceived(self, message):
        # print("eeee")
        error = QJsonParseError()
        # message=QJsonDocument.fromJson(message,error)
        # modify by chenqiwang start
        byte_array = QByteArray();
        byte_array.append(message)
        # print("Received JSON message ", message)
        log.info("Received JSON message "+message)
        rcv = QJsonDocument.fromJson(byte_array, error)
        # modify by chenqiwang end
        if error.error:
            print(
                "Failed to parse text message as JSON object:",
                message,
                "Error is:", error.errorString()
            )
            return
        elif not rcv.isObject():
            log.info("Received JSON message that is not an object: ", message)
            return
        # elf.messageReceived.emit("testssfsf")
        dict = {"a": "apple", "b": "banana", "g": "grape", "o": "orange"}
        # self.messageReceived.emit(dict,self)
        dict1 = {"type": 10, "id": 1};
        self.messageReceived.emit(dict1, self)
        # print("ffff")
        self.sendMessage(rcv)


class WebSocketClientWrapper(QObject):
    clientConnected = pyqtSignal(WebSocketTransport)

    def __init__(self, server, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._server = server
        self._server.newConnection.connect(self.handleNewConnection)

    @pyqtSlot()
    def handleNewConnection(self):
        self.clientConnected.emit(
            WebSocketTransport(self._server.nextPendingConnection())
        )


class Dialog(QDialog):
    sendText = pyqtSignal(str)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        l = QGridLayout(self)
        self.output = QPlainTextEdit(
            self,
            readOnly=True,
            plainText="Initializing WebChannel...")
        l.addWidget(self.output, 0, 0, 1, 2)

        self.input = QLineEdit(self, placeholderText="Message Contents")
        l.addWidget(self.input, 1, 0)

        self.send = QPushButton("Send", self, clicked=self.clicked)
        l.addWidget(self.send, 1, 1)

    def displayMessage(self, message):
        self.output.appendPlainText(message)

    @pyqtSlot(str)
    def receiveText(self, text):
        self.displayMessage("Received message: {}".format(text))
        log.info("receiveText:", "Received message: {}".format(text))

    @pyqtSlot()
    def clicked(self):
        text = self.input.text()
        if not len(text) or text.isspace(): return

        self.sendText.emit(text)
        self.displayMessage("Sent message: {}".format(text))

        self.input.clear()
def settting(object_settings):
    # setting
    # glob_settings = QtWebEngineWidgets.QWebEngineSettings.globalSettings()
    # Global web settings
    glob_settings=object_settings;
    glob_settings.setAttribute(1, True)  # JaveScript
    glob_settings.setAttribute(2, True)  # JaveScript can open window
    glob_settings.setAttribute(3, True)  # Clipboard (JaveScript)
    glob_settings.setAttribute(5, True)  # Local Storage
    glob_settings.setAttribute(6, True)  # LocalContentCanAccessRemoteUrls
    glob_settings.setAttribute(7, True)  # XSSAuditingEnabled
    glob_settings.setAttribute(9, True)  # LocalContentCanAccessFileUrls
    glob_settings.setAttribute(11, True)  # ScrollAnimatorEnabled
    glob_settings.setAttribute(14, True)  # FullScreenSupportEnabled

    # Check that the options are applied
    # print (object_settings.testAttribute(1))  # JaveScript
    # print (object_settings.testAttribute(2))  # JaveScript
    # print (object_settings.testAttribute(3))  # Clipboard (JaveScript)
    # print (object_settings.testAttribute(5))  # Local Storage
    # print (object_settings.testAttribute(6))  # LocalContentCanAccessRemoteUrls
    # print (object_settings.testAttribute(7))  # XSSAuditingEnabled
    # print (object_settings.testAttribute(9))  # LocalContentCanAccessFileUrls
    # print (object_settings.testAttribute(11))  # ScrollAnimatorEnabled
    # print (object_settings.testAttribute(14))  # FullScreenSupportEnabled
@pyqtSlot(QCloseEvent)
def closeEvent(self, event):
    # this.close()
    log.info("closeEvent")
    omClient.stop()
    # result = self.abstractNoScriptObject.getComponentRequestResponse().getResponse()
    # print("result: ", result)
    # QTextStream(stdout) << "c++result = " << result << "\r\n"
    event.accept()
    # self.wake.emit(result)
    # emit wake(result)

class WebForm(QtWebEngineWidgets.QWebEngineView):
    closeEvent = pyqtSignal(QCloseEvent)
    @pyqtSlot()
    def finish(self):
        self.closeEvent.emit(QCloseEvent())

def downloadRequested(download):
    # if(download.savePageFormat() != QtWebEngineWidgets.QWebEngineDownloadItem.UnknownSaveFormat):
    try:
        log.info(download.path());
        filename, ok2 = QFileDialog.getSaveFileName(dialog, "下载",download.path(), 'File (*.*)');
        download.setPath(filename);
        download.accept();
        download.stateChanged.connect(doDownload)
    except:
        info = sys.exc_info()
        print(info[0], ":", info[1], ":", info[2])
        traceback.print_tb(info[2], limit=1, file=sys.stdout)
def doDownload(download):
    # log.info(download.path());
    log.info("download finished");
    # filename = download.path();
    # pos = filename.rfind("/")
    # if not filename[:pos] == "":
    #     os.startfile(filename[:pos]);  # 打开目录
if __name__ == "__main__":
    from sys import argv, exit

    a = QApplication(argv)

    server = QWebSocketServer(
        "QWebChannel Standalone Server",
        QWebSocketServer.NonSecureMode
    )
    if not server.listen(QHostAddress.LocalHost, 12345):
        log.error("监听端口 12345 失败,客户端已经打开...")
        exit(1)

    clientWrapper = WebSocketClientWrapper(server)

    channel = QWebChannel()
    clientWrapper.clientConnected.connect(channel.connectTo)

    dialog = Dialog()
    channel.registerObject("dialog", dialog)
    #========================初始化OMServer 连接=============================
    omClient=OMClient("omClient");
    omClient.start();
    # url=QUrl.fromLocalFile("./index.html");
    # url.setQuery("webChannelBaseUrl="+server.serverUrl().toString())
    # QDesktopServices.openUrl(url);

    # dialog.displayMessage(
    #     "Initialization complete, opening browser at {}.".format(
    #         url.toDisplayString()
    #     )
    # )
    # dialog.show()
    # dialog.raise_()

    app = QApplication(sys.argv)
    app.setApplicationName("美莱")
    app.setApplicationVersion("1.0")
    app.setApplicationDisplayName("MyLike P2 Client V2.2")

    webView = WebForm();
    #设置窗口大小
    #webView.showFullScreen()
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    webView.resize(rect.width(), rect.height()-36)
    dir = app.applicationDirPath();
    #设置图标
    app.addLibraryPath("./icon");
    app.setWindowIcon(QIcon("./icon/m.ico"));
    #conf
    url =  config.get("baseconf", "url")
    #url="http://127.0.0.1:8080/MylikeOMS/a/login";
    settting(webView.page().settings());
    webView.show()
    #注册关闭事件
    webView.closeEvent.connect(closeEvent)
    #注册下载事件
    webView.page().profile().downloadRequested.connect(downloadRequested);
    webView.load(QtCore.QUrl(url+"?webChannelBaseUrl=" + server.serverUrl().toString()))
    omClient.send("OT", "EXTID")
    exit(a.exec_())
