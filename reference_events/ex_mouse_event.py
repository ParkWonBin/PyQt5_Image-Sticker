import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusbar = self.statusBar()
        self.lable = QLabel(self)
        self.lable.resize(120,20)

        # 트레킹 확인
        # print(self.hasMouseTracking())
        self.setMouseTracking(True) # False : 클릭하면 위치 찾음. True : 클릭 안할 떄도 찾음.
        # print(self.hasMouseTracking())

        self.setGeometry(300,200,400,200)
        self.show()
    
    def mouseMoveEvent(self,event):
        txt = f"Mouse 위치 \nevent : x = {event.x()}, y = {event.y()} \nglobal: x = {event.globalX()}, y = {event.globalY()}"
        self.statusbar.showMessage(txt)
        
    def mousePressEvent(self,event):
        buttons = event.buttons()
        if   buttons & Qt.LeftButton:  btn ='LeftButton'
        elif buttons & Qt.RightButton: btn ='RightButton'
        elif buttons & Qt.MidButton:   btn ='MidButton'
        self.lable.setText(f"{btn} clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())