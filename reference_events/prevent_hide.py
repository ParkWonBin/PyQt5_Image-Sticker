from PyQt5 import QtGui, QtCore

class Window(QtGui.QWidget):
       def __init__(self):
           QtGui.QWidget.__init__(self)

       def changeEvent(self, event):
           if event.type() == QtCore.QEvent.WindowStateChange:
               if self.windowState() & QtCore.Qt.WindowMinimized:
                   print('changeEvent: Minimised')
               elif event.oldState() & QtCore.Qt.WindowMinimized:
                   print('changeEvent: Normal/Maximised/FullScreen')
           QtGui.QWidget.changeEvent(self, event)

if __name__ == '__main__':

       import sys
       app = QtGui.QApplication(sys.argv)
       window = Window()
       window.resize(300, 300)
       window.show()
       sys.exit(app.exec_())