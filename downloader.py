from PyQt5.QtCore import *;
from PyQt5.QtNetwork import *;
from log_util import LogUtil;

import math
import sys
import html
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog
from PyQt5.QtCore import (QDate, QRectF, Qt)
from PyQt5.QtWidgets import (QApplication,QDialog,
        QHBoxLayout,QPushButton, QTableWidget, QTableWidgetItem,QVBoxLayout)
from PyQt5.QtGui import (QFont,QFontMetrics,QPainter,QTextCharFormat,
                         QTextCursor, QTextDocument, QTextFormat,
                         QTextOption, QTextTableFormat,
                         QPixmap,QTextBlockFormat)
import urllib.request;
import  os;
class Downloader(QObject):
    def __init__(self,url, fileName,parent=None):
        super(Downloader, self).__init__(parent)
        self.manager = QNetworkAccessManager();
        self.manager.finished.connect(self.replyFinished)
        self.fileName = fileName;
        self.url = url;
    def download(self):
        # manager = QNetworkAccessManager();
        # self.connect(self.manager, pyqtSignal("finished(QNetworkReply *)"), self.replyFinished)
        # connect(self.manager, SIGNAL('finished()'), self, SLOT('replyFinished()'))
        # self.manager.finished.connect(self.replyFinished)
        # reply = self.manager.get(QNetworkRequest(QUrl(self.url)));
        self.manager.get(QNetworkRequest(QUrl(self.url)));


    @pyqtSlot(QNetworkReply)
    def replyFinished(self,reply):
        if(reply.error()):
            LogUtil.error(reply.errorString())
        else:
            file =  QFile(self.fileName);
            if file.open(QIODevice.WriteOnly):
                file.write(reply.readAll());
                file.flush();
                file.close();
        reply.deleteLater();
        reply.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # downloader = Downloader("https://gss1.bdstatic.com/-vo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=304ad8f708f41bd5da53eff269e1e6f6/d439b6003af33a87a4043fc6c05c10385243b584.jpg",'C:/1.jpg')
    # downloader.download()
    urllib.request.urlretrieve("https://gss1.bdstatic.com/-vo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=304ad8f708f41bd5da53eff269e1e6f6/d439b6003af33a87a4043fc6c05c10385243b584.jpg", 'C:/1.jpg')
    exit(app.exec_())