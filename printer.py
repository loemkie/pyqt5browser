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
# import qrc_resources

from PyQt5.QtCore import QSizeF
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog
from PyQt5.QtCore import (QDate, QRectF, Qt)
from PyQt5.QtWidgets import (QApplication,QDialog,
        QHBoxLayout,QPushButton, QTableWidget, QTableWidgetItem,QVBoxLayout)
from PyQt5.QtGui import (QFont,QFontMetrics,QPainter,QTextCharFormat,
                         QTextCursor, QTextDocument, QTextFormat,
                         QTextOption, QTextTableFormat,
                         QPixmap,QTextBlockFormat)
# import qrc_resources
DATE_FORMAT = "MMM d, yyyy"

class Printer(QDialog):

    def __init__(self, parent=None):
        super(Printer, self).__init__(parent)

        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.Letter)
        self.setWindowTitle("Printing")


    def printViaHtml(self,htmltext):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            # print(self.printer.logicalDpiX())
            # print(self.printer.logicalDpiX() * (210 / 25.4))
            # print(self.printer.logicalDpiY())
            # print(self.printer.logicalDpiY() * (297 / 25.4))
            # document.setPageSize(QSizeF(self.printer.logicalDpiX() * (210 / 25.4),
            #                             self.printer.logicalDpiY() * (297 / 25.4)));
            document.setHtml(htmltext)
            document.print_(self.printer)
    #打印小票
    def printReciept(self,htmltext):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            # print(self.printer.logicalDpiX())
            # print(self.printer.logicalDpiX() * (210 / 25.4))
            # print(self.printer.logicalDpiY())
            # print(self.printer.logicalDpiY() * (297 / 25.4))
            #A4
            # document.setPageSize(QSizeF(self.printer.logicalDpiX() * (210 / 25.4),self.printer.logicalDpiY() * (297 / 25.4)));
            #小票
            qsizeF = QSizeF(self.printer.logicalDpiX() * (257 / 25.4), self.printer.logicalDpiY() * (125 / 25.4));
            # qsizeF = QSizeF(self.printer.logicalDpiX() * (215.90 / 25.4), self.printer.logicalDpiY() * (127.00 / 25.4));
            # qsizeF = QSizeF(self.printer.logicalDpiY() * (125 / 25.4),self.printer.logicalDpiX() * (257 / 25.4));
            self.printer.setPageSize(QPrinter.Custom)
            self.printer.setPaperName("小票2")
            paperSize = QSizeF(257, 125);
            self.printer.setPaperSize(paperSize, QPrinter.Millimeter)
            # self.printer.setPageSizeMM(qsizeF)

            document.setPageSize(qsizeF);
            # font = QFont();
            # font.setPointSize(6)
            # document.setDefaultFont(font);
            document.setHtml(htmltext)
            document.print_(self.printer)
            # document.setPageSize(QSizeF(self.printer.logicalDpiX() * (255 / 25.4), self.printer.logicalDpiY() * (125 / 25.4)));
            # document.setHtml(htmltext)
            # document.print_(self.printer)