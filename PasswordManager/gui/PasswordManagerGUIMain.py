from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QFrame, QLabel, QGridLayout, QLineEdit, QPushButton, QCheckBox, QSizePolicy, QWidget,QLayout,QApplication,QAction
from PasswordManager.GeneralFunctions import center
from PasswordManager.States import States
from PasswordManager.PasswordManagerMainGUI import PasswordManagerMainGUI
from PasswordManager.PasswordDB import getFilePathGui,getPasswordFromGui
import sys

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
# close = False
# if app is None:
try:
    app = QApplication(sys.argv)
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook
    path = getFilePathGui()
    password = getPasswordFromGui()
    mainGui = PasswordManagerMainGUI(password,path)
    app.exec()
    app.exit()
except Exception as e:
    print(e)

# else:
#     mainGui = PasswordManagerMainGUI()
#     app.exec()

