import sys
from time import sleep

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QImage, QPixmap, QPaintEvent
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia



class myLabel(QtWidgets.QLabel):  # 自定义的QLabel类

    def __init__(self, parent=None):
        super(myLabel, self).__init__(parent)
        layout = QVBoxLayout()
        self.btn = QPushButton()
        self.btn.clicked.connect(self.loadFile)
        self.btn.setText("从文件中获取照片")
        layout.addWidget(self.btn)
        self.label = QLabel()
        layout.addWidget(self.label)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        # 左键按下
        if e.buttons() == QtCore.Qt.LeftButton:
            # self.setText("左")
            print((e.x(), e.y()))

    def loadFile(self):
        self.label.setPixmap(QPixmap("black.png"))

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.label = myLabel()
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pil_image = QImage('timg.jpg')



        self.initUI()
        # self.paintEvent()

    def initUI(self):
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
