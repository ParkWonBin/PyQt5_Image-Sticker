
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QDragEnterEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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

def dragEnterEvent(self, e: QDragEnterEvent):
    e.accept()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

