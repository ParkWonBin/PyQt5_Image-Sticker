import sys
from PyQt5.QtGui import QImage,QPainter,QMovie
from PyQt5.QtCore import Qt, QPoint, QByteArray,QSize
from PyQt5.QtWidgets import QWidget,QMainWindow,QVBoxLayout,QApplication,QLabel

# 이미지 크기 조정 관련
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QImage()
        self.play_gif('earth.gif')

    def play_gif(self,gif_url):
        # gif 영상 관련
        self.movie = QMovie(gif_url, QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.start()
        self.movie.loopCount()

    def paintEvent(self, event):
        qp = QPainter(self)
        if not self.image.isNull():
            image = self.image.scaled(self.size())
            qp.drawImage(0, 0, image)

class Window(QMainWindow):
    def __init__(self) :
        super().__init__()

        # 이미지 관련
        self.is_gif = False
        self.canvas = Canvas()
        self.setWindowTitle("image-sticker")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAcceptDrops(True)


        # 이미지 배치
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)
        self.canvas.image = QImage("image.jpg")

        size = self.canvas.image.size()
        self.resize_window(size.width(),size.height())
        ####################
        self.movie_screen = QLabel(self.canvas) # 위젯 겹치기
        self.movie_screen.move(0,0)
        self.movie_screen.hide() # 기본값: hide
        #######################

    # 마우스 이벤트 관련
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.mouseButtonKind(event.buttons())

    # 좌/우/중 클릭 : 이동/크기/종료
    def mouseMoveEvent(self, event):
        # 마우스 움직인 정도
        delta = QPoint(event.globalPos() - self.oldPos)

        if self.is_clicked_L :
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else :
            self.resize_window(self.width()+delta.x(),self.height()+delta.y())
        self.oldPos = event.globalPos()

    def resize_window(self,x,y):
        self.resize(x,y)
        if self.is_gif:
            size = QSize(x,y)
            self.movie_screen.resize(size)
            self.movie_screen.movie().setScaledSize(size)

    def mouseButtonKind(self,buttons):
        if buttons & Qt.LeftButton:
            self.is_clicked_L =True
        if buttons & Qt.RightButton:
            self.is_clicked_L =False
        if buttons & Qt.MidButton:
            sys.exit(app.exec_())

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        img_url = event.mimeData().text().lstrip("file:///")

        if img_url[-4:]=='.gif':
            self.is_gif=True
            self.movie_screen.show()
            self.canvas.play_gif(img_url)
            self.movie_screen.setMovie(self.canvas.movie)
            self.canvas.image = QImage()
            size = self.geometry()

        else:
            self.is_gif =False
            self.canvas.image = QImage(img_url)
            self.movie_screen.hide()
            size = self.canvas.image.size()
        self.resize_window(size.width(), size.height())
        self.canvas.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())