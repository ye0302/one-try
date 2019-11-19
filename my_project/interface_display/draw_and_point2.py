import sys
from time import sleep

from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPainter, QBrush, QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia


class myLabel(QtWidgets.QLabel):  # 自定义的QLabel类

    def __init__(self, parent=None):
        super(myLabel, self).__init__(parent)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        # 左键按下
        if e.buttons() == QtCore.Qt.LeftButton:
            # self.setText("左")
            print(e.x()-8,e.y()-8)



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.label = myLabel()
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pil_image = QImage('timg.jpg')
        self.initUI()

    def initUI(self):
        # self.draw_other_picture()
        w, h = self.pil_image.width(), self.pil_image.height()  # 获取图片大小
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
    app.exec_()
    sys.exit()
