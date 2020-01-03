from PyQt5.QtWidgets import QApplication
from win32api import GetSystemMetrics


def center(windowObj):
    frameGm = windowObj.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    centerPoint = QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    windowObj.move(frameGm.topLeft())