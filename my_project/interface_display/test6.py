from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia


class myLabel(QtWidgets.QLabel):  # 自定义的QLabel类

    def __init__(self,parent=None):
        super(myLabel, self).__init__(parent)


    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        # 左键按下
        if e.buttons() == QtCore.Qt.LeftButton:
            # self.setText("左")
            print((e.x(),e.y()))



class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.label = myLabel()
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
