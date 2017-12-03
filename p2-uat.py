# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import  *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys

from ctypes import *
import ctypes
import os

app = QApplication(sys.argv)
app.setApplicationName("美莱")
app.setApplicationVersion("1.0")
app.setApplicationDisplayName("mylike")
webView = QtWebEngineWidgets.QWebEngineView()
webView.show()
try:
    dll = ctypes.windll.LoadLibrary(os.getcwd()+"/dll/Termb.dll")


    dll.CVR_InitComm(1001)
    dll.CVR_Authenticate()
    dll.CVR_Read_Content(1)
    f = open(os.getcwd()+"/dll/wz.txt",'r',encoding= 'gbk')
    txt = f.read()
    info=txt.split("\n")
    print(info[0])
    webView.page().runJavaScript("receiveDia('" +info[0] + "')")
finally:
    webView.page().runJavaScript("receiveDia('读卡失败')")
webView.load(QtCore.QUrl("http://www.baidu.com"))

sys.exit(app.exec_())