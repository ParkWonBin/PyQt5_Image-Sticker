
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap,QPainter
from PyQt5.QtCore import Qt, QPoint


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_clicked_left =True

    def initUI(self):
        # 타이틀 영역 제거 
        self.setWindowFlag(Qt.FramelessWindowHint) 
        
        # 이미지 선택
        self.pixmap = QPixmap("image.jpg")
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.pixmap)

        # 이미지 얹기
        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_img)
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
        
        if self.is_clicked_left :
            # 위치 조절
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else :
            # 크기 조절
            w = self.width() +delta.x()
            h = self.height()+delta.y()
            self.pixmap = self.pixmap.scaled(w,h, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.lbl_img.setPixmap(self.pixmap)
            self.resize(w,h)

        self.oldPos = event.globalPos()

    def mouseButtonKind(self,buttons):
        if buttons & Qt.LeftButton: self.is_clicked_left =True
        if buttons & Qt.RightButton:self.is_clicked_left =False
        if buttons & Qt.MidButton:  sys.exit(app.exec_())


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())


# 마우스 버튼 이벤트 관련
# https://freeprog.tistory.com/330