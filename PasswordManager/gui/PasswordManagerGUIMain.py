from PyQt5.QtWidgets import QApplication
from PasswordManager.PasswordManagerMainGUI import PasswordManagerMainGUI
from PasswordManager.PasswordDB import getFilePathGui,getPasswordFromGui
import sys

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
# close = False
# if app is None:
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

# else:
#     mainGui = PasswordManagerMainGUI()
#     app.exec()

