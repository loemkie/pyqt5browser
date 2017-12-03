import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

# class WebPage(QtWebEngineWidgets.QWebEnginePage):
#     def chooseFiles(self, mode, oldfiles, mimetypes):
#         print('Called this')
#         return []

class Window(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super(Window, self).__init__()
        self.setPage(QtWebEngineWidgets.QWebEnginePage(self))
        self.setHtml('<input type="file">')

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # .setGeometry(600, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())