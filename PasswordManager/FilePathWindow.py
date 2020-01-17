from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QLineEdit, QFileDialog
from PasswordManager.GeneralFunctions import center
from PasswordManager.FileManager import defaultFilePath
from PyQt5.QtWidgets import QApplication
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class FilePathWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.filePath = defaultFilePath
        self.title = 'Path chooser'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
        self.close()
#---------------------------------------------------------------------------------------
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        center(self)
        buttonReply = QMessageBox.question(self, "Path to file",'Do you want to use default path?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.openDialogBox()
#---------------------------------------------------------------------------------------
    def openDialogBox(self):
        userInput = QFileDialog()
        userInput.setFileMode(QFileDialog.ExistingFile)
        userInput = userInput.getOpenFileName(self, "Select Directory")[0]
        if len(userInput) > 0:
            self.filePath = userInput
#---------------------------------------------------------------------------------------
    def getFilePath(self):
        return self.filePath
#---------------------------------------------------------------------------------------



