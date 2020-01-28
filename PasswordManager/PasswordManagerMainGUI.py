from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QGridLayout, QWidget,QTableWidget, QMenuBar,QVBoxLayout,QMainWindow,QAction\
,QTableWidgetItem,QSizePolicy,QAbstractScrollArea,QStyledItemDelegate,QMessageBox,QItemDelegate,QApplication,QInputDialog,QLineEdit,QDialog
from PyQt5.QtCore import QThread
from itertools import cycle
from PasswordManager.GeneralFunctions import center
from PasswordManager.States import States
from PasswordManager.PasswordDB import PasswordDB,getFieldsList
from PasswordManager.AddAccountFrame import AddAccountFrame,GuiPasswordWindow
from PasswordManager.Cipher import Cipher
from PasswordManager.Account import Fields
import inspect
import time
import copy

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self,*args,**kwargs):
        super(MyQTableWidgetItem, self).__init__(*args,**kwargs)
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class VisibilityDelegate(QStyledItemDelegate,QItemDelegate):
    visibilityRole = QtCore.Qt.UserRole + 1000
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if not index.data(self.visibilityRole) and index.column() > 0:
            option.text = "*" * len(option.text)
    # def editorEvent(self, QEvent, QAbstractItemModel, QStyleOptionViewItem, QModelIndex):
    #     super().editorEvent(QEvent, QAbstractItemModel, QStyleOptionViewItem, QModelIndex)
    #     return False
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delegate = VisibilityDelegate(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.debug = False
        self.pwDB = None
        self.tableList = None
        self.allowDataEdition = False
        self.dataSaved = True
        self.deleteConfirmation = None
        self.accNameHelpList = None
        self.dataChangeCancelation = False
        self.sideTask = None
        self.showPassword = None
        self.visibility_index = QtCore.QModelIndex()
        self.setItemDelegate(delegate)
        self.pressed.connect(self.on_pressed)
#---------------------------------------------------------------------------------------
    def setDeleteConfirmation(self,deleteConfirmation):
        self.deleteConfirmation = deleteConfirmation
#---------------------------------------------------------------------------------------
    def showDebug(self):
        if self.debug:
            print(inspect.stack()[1][3])
#---------------------------------------------------------------------------------------
    def dataChanged(self, *args, **kwargs):
        self.showDebug()
        if self.allowDataEdition:
            row = args[0].row()
            col = args[0].column()
            newValue = args[0].data()
            accOldName = self.accNameHelpList[row]
            if col == 0:
                if self.dataChangeCancelation:
                    self.dataChangeCancelation = False
                    return None
                else:
                    if newValue in self.accNameHelpList:
                        QMessageBox.information(self,"Error","Account with that name already exists.")
                        self.dataChangeCancelation = True
                        item = MyQTableWidgetItem(accOldName)
                        self.setItem(row, col, item)
                        return None
                    self.allowDataEdition = False
                    oldAcc = self.pwDB.getAccount(accOldName)
                    newAcc = oldAcc.__copy__()
                    newAcc.changeAccountFieldValue(Fields.NAME,newValue)
                    self.removeAndAddAcc(oldAcc,newAcc)
            else:
                oldAcc = self.pwDB.getAccount(accOldName)
                self.removeAccAndUpdateTable(oldAcc,updateTable=False)
                oldAcc.changeAccountFieldValue(Fields().getFromNum(col),newValue)
                self.saveAccToFileAndUpdateTable(oldAcc)

#---------------------------------------------------------------------------------------
    def removeAndAddAccTask(self,oldAcc,newAcc):
        self.showDebug()
        try:
            self.removeAccAndUpdateTable(oldAcc, updateTable=False)
            self.saveAccToFileAndUpdateTable(newAcc)
        except Exception as e:
            print(e)
    def removeAndAddAcc(self, oldAcc, newAcc):
        self.showDebug()
        try:
            while self.sideTask is not None and self.sideTask.isRunning():
                time.sleep(0.250)
            self.sideTask = FileManagerSideThread(task=self.removeAndAddAccTask, taskVal=(oldAcc,newAcc), parent=self)
            self.sideTask.start()
            self.sideTask.wait(5)
        except Exception as e:
            print(e)
#---------------------------------------------------------------------------------------
    def setTableValues(self):
        self.showDebug()
        self.setRowCount(len(self.tableList))
        self.accNameHelpList = []
        x = 0
        for acc in self.tableList:
            y = 0
            for val in acc.getValuesAsList():
                if isinstance(val,Cipher):
                    val = val.getDecrypted()
                    if not self.showPassword.isChecked():
                        val = "*"*len(val)
                else:
                    self.accNameHelpList.append(val)
                item = MyQTableWidgetItem(val)

                self.setItem(x,y,item)
                y += 1
            x += 1
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.allowDataEdition = True
#---------------------------------------------------------------------------------------
    def setPwDBObj(self,pwdb):
        self.pwDB = pwdb
        self.tableList = self.pwDB.getAccountSet()
#---------------------------------------------------------------------------------------
    def mousePressEvent(self, event):
        self.allowDataEdition = False
        super(TableWidget,self).mousePressEvent(event)
#---------------------------------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        self.allowDataEdition = True
        super(TableWidget,self).mouseReleaseEvent(event)
#---------------------------------------------------------------------------------------
    def keyPressEvent(self,event):
        super(TableWidget, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:
            columnNom = self.currentIndex().column()
            if columnNom == 0:
                accName = self.currentItem().text()
                if self.deleteConfirmationWindow(accName):
                    acc = self.pwDB.getAccount(accName)
                    self.removeAccAndUpdateTable(acc)
        # elif event.key() == QtCore.Qt.Key_Enter or event.key() == 16777220: # 16777220 basic enter
#---------------------------------------------------------------------------------------
    def removeAccAndUpdateTable(self, acc, updateTable = True):
        self.showDebug()
        sideTask = FileManagerSideThread(task=self.pwDB.removeAccount, taskVal=acc, parent=self)
        sideTask.start()
        sideTask.wait(5)
        if updateTable:
            self.allowDataEdition = False
            self.setTableValues()

#---------------------------------------------------------------------------------------
    def saveAccToFileAndUpdateTable(self, acc, updateTable=True):
        self.showDebug()
        sideTask = FileManagerSideThread(task=self.pwDB.addAccount, taskVal=acc, parent=self)
        sideTask.start()
        sideTask.wait(5)
        if updateTable:
            self.allowDataEdition = False
            self.setTableValues()
    def hideTableValue(self):
        self.allowDataEdition = False
        for column in range(0,self.rowCount()):
            for row in range(1,4):
                item = self.item(column,row)
                item = MyQTableWidgetItem("*"*len(item.data(0)))
                self.setItem(column,row,item)
        self.allowDataEdition = True
#---------------------------------------------------------------------------------------
    def showTableValue(self):
        self.allowDataEdition = False
        for row in range(0,self.rowCount()):
            name = self.item(row,0).data(0)
            acc = self.pwDB.getAccount(name)
            for column in range(1,4):
                item = MyQTableWidgetItem(acc.getValueByField(Fields().getFromNum(row)))
                self.setItem(row,column,item)
        self.allowDataEdition = True
#---------------------------------------------------------------------------------------
    def deleteConfirmationWindow(self,accName):
        if not self.deleteConfirmation:
            return True
        else:
            buttonReply = QMessageBox.question(self, f"Removal confirmation", f'You sure you want to delete account {accName}',
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                return True
            else:
                return False
    #---------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_pressed(self, index):
        if self.visibility_index.isValid():
            self.model().setData(self.visibility_index, False, VisibilityDelegate.visibilityRole)
        self.visibility_index = index
        self.model().setData(self.visibility_index, True, VisibilityDelegate.visibilityRole)
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class PasswordManagerMainGUI(QMainWindow):
    def __init__(self,password, filePath):
        super().__init__()
        self.pwDB = PasswordDB(password=password,pathToDbFile=filePath,debug=True)
        self.setCentralWidgetWindow()
        self.mainGrid = QVBoxLayout()            # type: QGridLayout
        # self.hSize = 400
        # self.wSize = 800
        # self.resize(self.wSize,self.hSize)
        # self.setMinimumSize(self.wSize, self.hSize)
        # self.setFixedSize(self.wSize, self.hSize)
        self.deleteConfirmationValue = True

        self.setWindowTitle("GUI PasswordManager")
        self.populateGrid()


        self.centralWindow.setLayout(self.mainGrid)
        self.setCentralWidget(self.centralWindow)
        self.table.allowDataEdition = True
        self.state = States.UNDEFINE

        center(self)

        self.show()
        self.setFocus(QtCore.Qt.ActiveWindowFocusReason)
#---------------------------------------------------------------------------------------
    def setCentralWidgetWindow(self):
        self.centralWindow = QWidget()
        self.centralWindow.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
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
    def addAccountAction(self):
        AddAccountFrame(fun=self.table.saveAccToFileAndUpdateTable,currentAccList=self.table.accNameHelpList)
#---------------------------------------------------------------------------------------
    def addMenuBar(self):
        self.menuBar = QMenuBar()
        self.options = self.menuBar.addMenu("Options")     # type:QMenuBar
        addAccountAction = QAction("Add Account",self)
        addAccountAction.triggered.connect(self.addAccountAction)
        self.options.addAction(addAccountAction)

        changeMainPassword = QAction("Change main password", self)
        changeMainPassword.triggered.connect(self.changeMainPassword)
        self.options.addAction(changeMainPassword)

        self.removeAccountAction = QAction("Remove Account Confirmation", self, checkable=True)
        self.removeAccountAction.setChecked(True)
        self.removeAccountAction.triggered.connect(self.setDeleteConfirmationVal)
        self.options.addAction(self.removeAccountAction)

        self.showPasswordOption = QAction("Show data on edit", self, checkable=True)
        self.showPasswordOption.setChecked(False)
        self.showPasswordOption.triggered.connect(self.showDataOnEdit)
        self.options.addAction(self.showPasswordOption)

        self.setMenuBar(self.menuBar)
#---------------------------------------------------------------------------------------
    def showDataOnEdit(self):
        if self.showPasswordOption.isChecked():
            self.table.showTableValue()
        else:
            self.table.hideTableValue()
#---------------------------------------------------------------------------------------
    def changeMainPassword(self):
        password = NewPassword()
        password,ok = password.getText()
        if ok:
            pwLen = len(password)
            if pwLen == 0 or pwLen > 32:
                QMessageBox().information(self,"Password change","Password lenght is incorent\nMin 1 char max 32 chars.")
            else:
                self.pwDB.changeMainPassword(password)
                QMessageBox().information(self,"Password change","Password changed successfully")
#---------------------------------------------------------------------------------------
    def setDeleteConfirmationVal(self):
        self.table.setDeleteConfirmation(self.removeAccountAction.isChecked())
#---------------------------------------------------------------------------------------
    def populateGrid(self):
        self.addMenuBar()
        self.table = TableWidget()
        self.table.showPassword = self.showPasswordOption
        self.table.setPwDBObj(self.pwDB)
        self.table.setDeleteConfirmation(self.deleteConfirmationValue)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([x.capitalize()  for x in getFieldsList()])
        self.mainGrid.addWidget(self.table)
        self.table.setTableValues()
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
class FileManagerSideThread(QThread):
    def __init__(self,task=None,taskVal=None,parent=None):
        super(QThread,self).__init__()
        self.task = task
        self.taskVal = taskVal
#---------------------------------------------------------------------------------------
    def run(self):
        if isinstance(self.taskVal,tuple):
            self.task(self.taskVal[0],self.taskVal[1])
        else:
            self.task(self.taskVal)
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
class NewPassword(QDialog):
    def __init__(self):
        super(NewPassword,self).__init__()
        self.setGeometry(100,100,100,100)
        center(self)
    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Change password", "Enter new password:", QLineEdit.Password)
        return text,okPressed
