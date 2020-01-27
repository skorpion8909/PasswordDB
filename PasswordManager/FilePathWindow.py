from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QLineEdit, QFileDialog
from PasswordManager.GeneralFunctions import center
from PasswordManager.FileManager import defaultFilePath
from PyQt5.QtWidgets import QApplication
import os
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class FilePathWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.filePath = defaultFilePath
        self.title = 'Path chooser'
        self.configFileName = "passConf.conf"
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
        buttonReply = QMessageBox.question(self, "Path to file",'Do you want to use different then default file path location?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.openDialogBox()
        else:
            if os.path.exists(self.configFileName):
                with open(self.configFileName,"r") as file:
                    try:
                        path = file.readlines()[0].split("=")[1].strip(" ")
                        self.filePath = path
                    except Exception as e:
                        print(e)
                        print("Something wrong with "+self.configFileName+" file.")
                        print("Removing file...")
                        file.close()
                        os.remove(self.configFileName)
                        if os.path.exists(self.configFileName):
                            print("File was not removed.")
                        else:
                            print("File removed correctly.")
#---------------------------------------------------------------------------------------
    def openDialogBox(self):
        userInput = QFileDialog()
        userInput.setFileMode(QFileDialog.ExistingFile)
        userInput = userInput.getOpenFileName(self, "Select Directory")[0]

        if len(userInput) > 0:
            self.filePath = userInput
            if os.path.exists(self.configFileName):
                os.remove(self.configFileName)
            with open(self.configFileName, "w+") as file:
                toWr = "myDB.pass-path = "+self.filePath.strip(" ")
                file.write(toWr)
#---------------------------------------------------------------------------------------
    def getFilePath(self):
        return self.filePath
#---------------------------------------------------------------------------------------



