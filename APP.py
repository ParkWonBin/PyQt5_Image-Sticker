
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 타이틀 영역 제거 
        self.setWindowFlag(Qt.FramelessWindowHint) 
        
        # 이미지 선택
        pixmap = QPixmap("image.jpg")
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)

        # 이미지 얹기
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.setContentsMargins(0,0,0,0)
        self.setLayout(vbox)

        # 위치 조정
        self.move(300, 300)
        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.mouseButtonKind(event.buttons())
        # print(event)

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos) # 마우스 움직인 정도
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseButtonKind(self,buttons):
        if buttons & Qt.LeftButton: 
            print('LeftButton')
        if buttons & Qt.RightButton: 
            print('RightButton')
        if buttons & Qt.MidButton: 
            print('MidButton')

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())


# 마우스 버튼 이벤트 관련
# https://freeprog.tistory.com/330