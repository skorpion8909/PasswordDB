from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QFrame, QLabel, QGridLayout, QLineEdit, QPushButton, QCheckBox, QSizePolicy, QWidget,QLayout,QApplication,QAction,QDialog,QMessageBox
from PasswordManager.GeneralFunctions import center
from PasswordManager.Account import Account
from PasswordManager.States import States
from PasswordManager.Cipher import Cipher
from PasswordManager.States import States
import sys

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class AddAccountFrame(QWidget):
    def __init__(self,accName="",fun=None,currentAccList=None):
        super().__init__()
        self.fun = fun
        self.currentAccList = currentAccList
        self.accName = accName                   # type: NagiosConnectionManager
        self.mainGrid = QGridLayout()            # type: QGridLayout
        self.mainGrid.setSizeConstraint(QLayout.SetMinimumSize)
        self.wSize = 450
        self.hSize = 180
        self.setMinimumSize(self.wSize, self.hSize)
        self.setFixedSize(self.wSize, self.hSize)
        self.setWindowTitle("Adding account")
        self.password = Cipher("")
        self.populateGrid()
        self.account = None

        self.setLayout(self.mainGrid)
        self.state = States.UNDEFINE

        center(self)

        self.show()
        print("Show")
        self.setFocus(QtCore.Qt.ActiveWindowFocusReason)
#---------------------------------------------------------------------------------------
    #override closeEvent
    def closeEvent(self, event):
        if self.state == States.UNDEFINE:
            self.state = States.CLOSE
        event.accept()
#---------------------------------------------------------------------------------------
    def exitAction(self):
        self.state = States.CLOSE
#---------------------------------------------------------------------------------------
    def populateGrid(self):

        accNameLabel = QLabel("Account name: ")
        loginLabel = QLabel("Login: ")
        passwordLabel1 = QLabel("Password1: ")
        passwordLabel2 = QLabel("Password2: ")
        checkBoxLabel = QLabel("Remember me: ")
        checkBoxLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.loginEntry = QLineEdit()
        self.loginEntry.setPlaceholderText("login optional")

        self.accNameEntry = QLineEdit(self.accName)
        self.accNameEntry.setPlaceholderText("not optional")
        self.accNameEntry.textChanged.connect(self.nameEntryChanged)

        if len(self.accName) != 0:
            self.accNameEntry.setEnabled(False)


        self.passwordEntry1 = QLineEdit()
        self.passwordEntry1.setEchoMode(QLineEdit.Password)
        self.passwordEntry1.setPlaceholderText("password1 optional")

        self.passwordEntry2 = QLineEdit()
        self.passwordEntry2.setEchoMode(QLineEdit.Password)
        self.passwordEntry2.setPlaceholderText("password2 optional")

        self.passwordDBLabel = QLabel("PasswordDB:")
        self.passwordDBPasswordEntry = QLineEdit()
        self.passwordDBPasswordEntry.setEchoMode(QLineEdit.Password)
        self.passwordDBPasswordEntry.setMaxLength(32)
        self.passwordDBPasswordEntry.setPlaceholderText("password for encryption")

        self.rememberMeCheckBox = QCheckBox()
        self.rememberMeCheckBox.stateChanged.connect(lambda : self.checkBoxEvent())
        if self.fun is not None:
            self.rememberMeCheckBox.setEnabled(False)

        self.loginButton = QPushButton("Start")
        self.loginButton.clicked.connect(lambda x: self.startButtonClicked())

        self.mainGrid.addWidget(accNameLabel, 0, 0)
        self.mainGrid.addWidget(self.accNameEntry, 0, 1)
        self.mainGrid.addWidget(loginLabel,1,0)
        self.mainGrid.addWidget(self.loginEntry,1,1)
        self.mainGrid.addWidget(passwordLabel1,2,0)
        self.mainGrid.addWidget(self.passwordEntry1,2,1)
        self.mainGrid.addWidget(passwordLabel2,3,0)
        self.mainGrid.addWidget(self.passwordEntry2,3,1)
        self.mainGrid.addWidget(checkBoxLabel,4,0)
        self.mainGrid.addWidget(self.rememberMeCheckBox,4,1)
        self.mainGrid.addWidget(self.loginButton,5,0,2,2)

#---------------------------------------------------------------------------------------
    def nameEntryChanged(self,text):
        if self.currentAccList is not None:
            if True in [True if text == x else False for x in self.currentAccList]:
                self.loginButton.setEnabled(False)
                self.loginButton.setText("Account with this name already exist.")
            else:
                if not self.loginButton.isEnabled():
                    self.loginButton.setEnabled(True)
                    self.loginButton.setText("Start")

    #---------------------------------------------------------------------------------------
    def checkBoxEvent(self):
        if self.rememberMeCheckBox.checkState():
            self.resize(self.wSize, (self.hSize+30))
            self.setFixedSize(self.wSize, self.hSize+30)
            self.mainGrid.addWidget(self.passwordDBLabel,5,0)
            self.mainGrid.addWidget(self.passwordDBPasswordEntry,5,1)
            self.loginButton.setParent(None)
            self.mainGrid.addWidget(self.loginButton, 6, 0, 2, 2)
        else:
            self.resize(self.wSize, self.hSize)
            self.setFixedSize(self.wSize, self.hSize)
            self.passwordDBLabel.setParent(None)
            self.passwordDBPasswordEntry.setParent(None)
            self.mainGrid.addWidget(self.loginButton, 5, 0, 2, 2)
            if "Start" not in self.loginButton.text():
                self.loginButton.setText("Start")
#---------------------------------------------------------------------------------------
    def startButtonClicked(self):
        if self.rememberMeCheckBox.checkState():
            if len(self.passwordDBPasswordEntry.text()) == 0:
                self.loginButton.setText("PasswordDB field cannot be empty!")
                return None
        if len(self.accNameEntry.text()) == 0:
            self.loginButton.setText("Account name cannot be empty")
            return None
        self.setElementsEnableAtribute(False,"Ok")
        self.state = States.OK
        self.password = Cipher(self.passwordDBPasswordEntry.text())
        self.account = Account(self.accNameEntry.text(),self.loginEntry.text(),self.passwordEntry1.text(),self.passwordEntry2.text())
        if self.fun is not None:
            self.fun(self.getAccount())
        self.close()
#---------------------------------------------------------------------------------------
    def getAccount(self):
        return self.account
#---------------------------------------------------------------------------------------
#     def checkCreds(self):
#         # boolValue = self.ncm.checkCredentials(self.loginEntry.text(), self.passwordEntry.text())
#         boolValue = True
#         self.callbackAction(boolValue)
# #---------------------------------------------------------------------------------------
#     def callbackAction(self, boolValue):
#         if boolValue:
#             self.loginButton.setText("OK!")
#             if self.rememberMeCheckBox.checkState():
#                 self.pwDB.startFullInit(self.passwordDBPasswordEntry.text())
#                 acc = Account("Nagios",self.loginEntry.text(),self.passwordEntry1.text(),self.passwordEntry2.text())
#                 self.pwDB.addAccount(acc)
#         else:
#             self.setElementsEnableAtribute(True, "Try again")
#---------------------------------------------------------------------------------------
    def setElementsEnableAtribute(self,value,text):
        self.loginButton.setText(text)
        self.passwordEntry1.setEnabled(value)
        self.passwordEntry2.setEnabled(value)
        self.passwordDBPasswordEntry.setEnabled(value)
        self.rememberMeCheckBox.setEnabled(value)
        self.loginEntry.setEnabled(value)
        self.loginButton.setEnabled(value)
#---------------------------------------------------------------------------------------
    def getWindowState(self):
        return self.state
#---------------------------------------------------------------------------------------
    def getRememberMeValue(self):
        if self.rememberMeCheckBox.checkState() == 2:
            return True
        if self.rememberMeCheckBox.checkState() == 0:
            return False
#---------------------------------------------------------------------------------------
    def getPassword(self):
        return self.password.getDecrypted()
#---------------------------------------------------------------------------------------

class GuiPasswordWindow(QWidget):
    def __init__(self,parent = None):
        super(GuiPasswordWindow,self).__init__(parent=parent)
        self.setGeometry(150,150,250,130)
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.label = QLabel("Enter Password")
        font = self.label.font()
        font.setPointSize(16)
        self.label.setFont(font)
        self.password = QLineEdit()
        self.password.textChanged.connect(self.myEditLineTextChanged)
        self.password.setEchoMode(QLineEdit.Password)
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(lambda x : self.enter())
        self.okButton.setEnabled(False)
        self.okButtonClicked = False
        self.password.returnPressed.connect(self.okButton.click)
        layout = QGridLayout()
        layout.addWidget(self.label,0,0,QtCore.Qt.AlignCenter)
        layout.addWidget(self.password,1,0,QtCore.Qt.AlignTop)
        layout.addWidget(self.okButton,2,0,QtCore.Qt.AlignTop)
        self.setLayout(layout)
        center(self)
        self.show()
#---------------------------------------------------------------------------------------
    def myEditLineTextChanged(self,text):
        textLenght = len(text)
        print(textLenght)
        if textLenght > 0 and textLenght <= 32:
            if not self.okButton.isEnabled():
                if self.label.text() not in "Enter Password":
                    self.label.setText(f"Enter Password")
                self.okButton.setEnabled(True)
        else:
            self.label.setText(f"MAX 32 chars MIN 1 char!\nYou entered {textLenght}")
            if self.okButton.isEnabled():
                self.okButton.setEnabled(False)
#---------------------------------------------------------------------------------------
    def closeEvent(self, event):
        if not self.okButtonClicked:
            print("X(close) button pressed")
            sys.exit(0)
#---------------------------------------------------------------------------------------
    def getPassword(self):
        return self.password.text()
#---------------------------------------------------------------------------------------
    def enter(self):
        self.okButtonClicked = True
        self.close()