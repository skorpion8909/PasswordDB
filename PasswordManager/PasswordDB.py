"""
This module is general purpose module to store up login and passwords in encrypted files.
Through PasswordDB api, provides an easy way to save and load credentials,
which are encrypted with a user key.

The main class is PasswordDB. Only this class should be used directly.
Rest of classes from this module may not work properly alone.
"""
# Python 3.7.2
from PasswordManager.CryptoManager import CryptoManager
from PasswordManager.FileManager import FileManager
from PasswordManager.Account import Fields, Account, getFieldsList
from PasswordManager.AccountManager import AccountManager
from PasswordManager.AddAccountFrame import AddAccountFrame,GuiPasswordWindow
from PasswordManager.LoginFlags import LoginFlags
from PyQt5.QtWidgets import QApplication
import atexit
import sys
from getpass import getpass
#import logging

# try to install necessary libraries
# TODO:Gui password managing interface
# TODO: Does not allow acc with the same name
# try:
#     from PyQt5 import *
# except Exception:
#     print('You need PyQt5')
#     print("Trying to install")
#     install("PyQt5")
#     print("Installation completed")
#     from PyQt5 import *

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
class PasswordDB:
    """
    This is a main class for this module. Only this module should be used directly.
    Rest of classes from this module will not work alone properly.
    """
    def __init__(self,password=None,pathToDbFile=None,fullInit=True,flag=None):
        if flag == LoginFlags.CONSOLE:
            pw = input("Enter password: ")
            # pw = getpass("Enter password: ")
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            self.startFullInit(pw, pathToDbFile)
        elif flag == LoginFlags.GUI:
            pw = getPasswordFromGui()
            self.startFullInit(pw, pathToDbFile)
        elif fullInit and password != None:
            self.startFullInit(password, pathToDbFile)
#----------------------------------------------------------------------------------------------------------------
    def startFullInit(self, password, pathToDbFile=None):
        # init main objects and values
        self.saveFile = True  # if True then auto saves to file any added account
        self.cryptoManager = CryptoManager(password)  # class for managing encryption part
        self.fileManager = FileManager(pathToDbFile, self.cryptoManager)  # layer for file I/O operation
        self.accountManager = AccountManager(self.fileManager)  # class that manages accounts
        self.accountManager.setAutoSave(self.saveFile)
        # if num of lines is more then 0
        if sum(1 for line in open(self.fileManager.getFileFullPath())) != 0:
            # load existing accounts
            self.accountManager.loadAccount(self.fileManager.getDecryptedFileContentAsList())
#----------------------------------------------------------------------------------------------------------------
    def addAccount(self,acc):
        self.accountManager.addAccount(acc)
#----------------------------------------------------------------------------------------------------------------
    def setAutoSave(self, boolValue):
        self.saveFile = boolValue
        self.accountManager.setAutoSave(boolValue)
#----------------------------------------------------------------------------------------------------------------
    def getAccountSet(self):
        return self.accountManager.getSetAccounts()
#----------------------------------------------------------------------------------------------------------------
    def getAccount(self, accountName):
        acc = self.accountManager.getAccountByName(accountName)
        if acc == None:
            print(f"Nie znaleziono {accountName}")
        return acc
#----------------------------------------------------------------------------------------------------------------
    def getDbFileLocation(self):
        return self.fileManager.getFileFullPath()
#----------------------------------------------------------------------------------------------------------------
    def changeMainPassword(self,password):
        if len(password) == 0:
            raise ValueError("Password cannot be empty")
        self.fileManager.emptyDbFile()
        self.fileManager.prepareToResave(self.getAccountSet())
        self.fileManager.resaveDB()
        self.cryptoManager.changePassword(password)
        self.accountManager.resaveAccounts(password)
#----------------------------------------------------------------------------------------------------------------
    def closeDB(self):
        self.fileManager.closeFile()
#----------------------------------------------------------------------------------------------------------------
def openAddAccountGUI(accName = ""):
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)
        addAccFrame = AddAccountFrame(accName)
        app.exec()
        app.exit()
    else:
        addAccFrame = AddAccountFrame(accName)
        app.exec()
    return addAccFrame
#----------------------------------------------------------------------------------------------------------------

def getPasswordFromGui():
    app = QApplication(sys.argv)
    if app is None:
        gui = GuiPasswordWindow()
        app.exec()
        app.exit()
    else:
        gui = GuiPasswordWindow()
        app.exec()

    return gui.getPassword()