import sys
from PyQt5.QtGui import QImage, QPainter, QMovie,QPalette, QPen
from PyQt5.QtCore import Qt, QPoint, QByteArray, QSize,QEvent
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, QLabel, QGraphicsOpacityEffect

desk = """
    [ 여기 이미지/움짤을 끌어다넣어주세요 ]

       - 위치조절 : 좌클릭 + 드래그
       - 크기조절 : 우클릭 + 드래그
       - 사용종료 : 중클릭
       - 사진교체 : 드래그 앤 드롭
"""


# 이미지 크기 조정 관련
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QImage()
        self.movie = QMovie()

    def play_gif(self, gif_url):
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
    def __init__(self):
        super().__init__()

        self.is_gif = False
        self.canvas = Canvas()
        self.no_img = QImage()

        self.setAcceptDrops(True)
        self.setMinimumSize(25, 25)
        self.setWindowTitle("image-sticker")
        self.setWindowFlags(Qt.FramelessWindowHint)# | Qt.WindowStaysOnTopHint) #주석풀면 최상단 고정
        
        # 배경 투명 및 초기 설명창 
        self.setAttribute(Qt.WA_TranslucentBackground, True)# 창 투명하게 하기
        self.Desk = QLabel(desk, self.canvas)
        self.Desk.setStyleSheet("color: black;" 
                              "background-color: #FFFFFF;"
                              "border-style: solid;"
                              "border-width: 4px;"
                              "border-color: #AAAAAA")

        # 레이아웃 및 캔버스 배치
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)
        self.update_img('image.jpg')
        ####################
        self.movie_screen = QLabel(self.canvas)  # 위젯 겹치기
        self.movie_screen.move(0, 0)
        self.movie_screen.hide()  # 기본값: hide
        #######################

    def WindowStateChange(self, event):
        if self.isMinimized(): 
            self.showNormal()
            #  self.activateWindow()
        # https://stackoverflow.com/questions/12280815/pyqt-window-focus
        # https://stackoverrun.com/ko/q/2302286

    # def paintEvent(self, event=None):
    #     painter = QPainter(self)
    #     painter.setOpacity(0) # 배경 투명하게
    #     painter.setBrush(Qt.white)
    #     painter.setPen(QPen(Qt.white))   
    #     painter.drawRect(self.rect())

    def update_img(self, img_url):
        img = QImage(img_url)
        if not img.isNull():
            del(self.canvas.image)
            self.canvas.image = img
            size = self.canvas.image.size()
            self.resize_window(size.width(), size.height())
            self.Desk.hide()
        else:
            self.setGeometry(500, 270, 260, 120)
            self.Desk.show()

    # key 이벤트 추후 추가 예정
    # def keyPressEvent(self, e):
    #     #https://wikidocs.net/23755
    #     if e.key() == Qt.Key_Escape:
    #         self.close()
    #     elif e.key() == Qt.Key_F:
    #         self.showFullScreen()
    #     elif e.key() == Qt.Key_N:  
    #          self.showNormal()
    #     elif e.key() == Qt.Key_C:  
    #         print('new window')
    #         self.window = Window()
    #         self.window.show()

    # 마우스 이벤트 관련
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        buttons = event.buttons()
        if buttons & Qt.LeftButton: self.is_clicked_L = True
        if buttons & Qt.RightButton:self.is_clicked_L = False
        if buttons & Qt.MidButton:  self.exec_()

    # 좌/우/중 클릭 : 이동/크기/종료
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        if self.is_clicked_L:
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else:
            self.resize_window(self.width() + delta.x(), self.height() + delta.y())
        self.oldPos = event.globalPos()

    def resize_window(self, x, y):
        self.resize(x, y)
        if self.is_gif:
            size = QSize(x, y)
            self.movie_screen.resize(size)
            self.movie_screen.movie().setScaledSize(size)

    def dragEnterEvent(self, event):
        # 드롭다운 받으면 dropEvent 호출하는 이벤트
        if event.mimeData().hasText():event.acceptProposedAction()

    def dropEvent(self, event):
        img_url = event.mimeData().text().lstrip("file:///")
        self.update_img(img_url)

        if img_url[-4:] == '.gif':
            self.is_gif = True
            del(self.canvas.movie)
            self.movie_screen.show()
            self.canvas.image = self.no_img # 배경 그림 지우기
            self.canvas.play_gif(img_url)# gif movie 생성
            self.movie_screen.setMovie(self.canvas.movie)
            size = self.geometry()

        else:
            self.is_gif = False
            self.movie_screen.hide()
            size = self.canvas.image.size()
        self.resize_window(size.width(), size.height())
        self.canvas.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

    # 투명도 설정 
    # https://stackoverflow.com/questions/33982167/pyqt5-create-semi-transparent-window-with-non-transparent-children
