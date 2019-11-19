import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage




class FirstMainWin(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.initUI()

        # 设置窗口的尺寸

        self.setWindowTitle('显示图像')
        # self.status = self.statusBar()
        #
        # self.status.showMessage('只存在5秒的消息',5000)

    def initUI(self):
        self.resize(400, 300)
        self.move(300, 200)
        self.lbl = QLabel(self)
        self.pil_image = QImage('/home/tarena/桌面/壁纸/test.png')
        self.fcku(self.pil_image)

    def fcku(self, fckimage):
        pil_image = self.m_resize(self.width(), self.height(), fckimage)

        pixmap = QPixmap.fromImage(pil_image)
        self.lbl.resize(pil_image.width(), pil_image.height())
        self.lbl.setPixmap(pixmap)

    def m_resize(self, w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片

        w, h = pil_image.width(), pil_image.height()  # 获取图像的原始大小

        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h

        factor = min([f1, f2])

        width = int(w * factor)

        height = int(h * factor)

        return pil_image.scaled(width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('C:/Users/TECH013/Desktop/Pic/公司左上角logo.jpg'))
    main = FirstMainWin()
    main.show()

    sys.exit(app.exec_())
