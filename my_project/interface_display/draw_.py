import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QImage
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.pil_image = QImage('timg.jpg')
        self.initUI()

    def initUI(self):
        w, h = self.pil_image.width(), self.pil_image.height()#获取图片大小
        self.setGeometry(700, 200, w, h)
        self.setWindowTitle('Brushes')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.use_palette()
        qp.end()

    def use_palette(self):

        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(self.pil_image)))

        self.setPalette(window_pale)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
