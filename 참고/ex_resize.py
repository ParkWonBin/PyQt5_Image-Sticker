# 출처 : https://stackoverflow.com/questions/57875347/resizing-a-qwindow-to-fit-contents

from PyQt5 import QtCore, QtGui, QtWidgets
class Canvas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Expanding
        )
        self.image = QtGui.QImage()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        if not self.image.isNull():
            image = self.image.scaled(
                self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation
            )
            qp.drawImage(0, 0, image)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.label = QtWidgets.QLabel("foobar")
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.canvas)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        content = QtWidgets.QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)
        self.load_image("image.jpg")

    def load_image(self, filename):
        image = QtGui.QImage(filename)
        self.canvas.image = image
    
    def keyPressEvent(self, event):
        self.load_image("image.jpg")
        super().keyPressEvent(event)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

    # 