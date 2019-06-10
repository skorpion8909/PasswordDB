import os
from builtins import print
from ntpath import basename, split
import atexit
import sys
from cryptography.fernet import InvalidToken
from PasswordManager.Account import Account

dbModulePath, _ = split(__file__)

#----------------------------------------------------------------------------------------------------------------
class FileManager:
    """
        FileManager is a simple class that contains all methods involved in managing
        a file.
    """
    def __init__(self,pathToDbFile,cryptoManager):
        self.initialPath = pathToDbFile
        #init variables
        self.cryptoManager = cryptoManager          # type: CryptoManager
        self.fileRawContentAsList = []              # type: list
        self.dbFile = None                          # type: open
        # if there was non user input regarding the file directory
        if pathToDbFile == None:
            self.initStandardValues()
        else:
            self.initUserValues(pathToDbFile)
        # open file and keep open to the end of a program
        self.loadFile()

        # close file at exit of main program
        self.closeAtExit()
#----------------------------------------------------------------------------------------------------------------
    def getDecryptedFileContentAsList(self):
        """:return read lines from file: type: list"""
        fileContentList = []
        for line in self.fileRawContentAsList:
            decryptedLine = self.decryptLine(line)
            if isinstance(decryptedLine,str):
                fileContentList.append(decryptedLine)
        return fileContentList
#----------------------------------------------------------------------------------------------------------------
    def decryptLine(self,line):
        encryptedLine = line
        decryptedLine = ""
        for value in line.split(","):
            if len(value) != 0:
                try:
                    de = str(self.cryptoManager.decrypt(value))
                except InvalidToken:
                    return str(InvalidToken) + str(line)
                decryptedLine += f"{de},"
            decryptedLine.strip(",")
        return decryptedLine
#----------------------------------------------------------------------------------------------------------------
    def initUserValues(self, pathToDbFile):
        # get file directory and file name base on user input
        self.dbDirectory, self.fileName = self.getDirAndPath(pathToDbFile)
        self.dbDirectory = str(self.dbDirectory)
        self.fileName = str(self.fileName)
        self.pathToFile = os.path.normpath(os.path.join(self.dbDirectory, self.fileName))

#----------------------------------------------------------------------------------------------------------------
    def initStandardValues(self):
        # default file name is
        self.fileName = "myDB.pass"
        # default file location is
        self.dbDirectory = dbModulePath
        # path to a file
        self.pathToFile = os.path.normpath(os.path.join(self.dbDirectory, self.fileName))

#----------------------------------------------------------------------------------------------------------------
    def getDirAndPath(self,path):
        """
        :param path to main file:
        :return directory and file name:
        """
        directory, fileName = split(path)
        print("/--=")
        print(directory)
        print(fileName)
        print(")_")
        return directory, fileName
#---------------------------------------------------------------------------------------------------------------
    def errorTextFormat(self,userPath, path):
        if userPath:
            print("Your file could not be open or created.")
        else:
            print("Default file could not be open or created.")

        print(f"{path}")
        print("Probably not sufficient access or path for a file is invalid.")
#----------------------------------------------------------------------------------------------------------------
    def closeAtExit(self):
        atexit.register(self.closeFile)

#----------------------------------------------------------------------------------------------------------------
    def closeFile(self):
        try:
            self.dbFile.close()
        except Exception as e:
            print("Exception while closing a file")
            print(e)

#----------------------------------------------------------------------------------------------------------------
    def loadFile(self):
        fileExist = os.path.isfile(self.pathToFile)
        try:
            if fileExist:
                self.dbFile = open(file=self.pathToFile, mode="r+", encoding="ASCII")
            else:
                self.dbFile = open(file=self.pathToFile, mode="w+", encoding="ASCII")

        except Exception as e:
            print(e)
            self.errorTextFormat(None == self.initialPath, self.fileName)
            # not handled yet
            sys.exit(0)

        for encryptedLine in self.dbFile.readlines():
            self.fileRawContentAsList.append(encryptedLine)

#----------------------------------------------------------------------------------------------------------------
    def createDbFile(self):
        self.dbFile = open(file=self.pathToFile, mode="w+", encoding="ASCII")
#----------------------------------------------------------------------------------------------------------------
    def getFileFullPath(self):
        return self.pathToFile
#----------------------------------------------------------------------------------------------------------------
    def saveAccount(self, acc):
        self.saveToFile(self.getEncryptedLine(acc))
#----------------------------------------------------------------------------------------------------------------
    def getEncryptedLine(self,acc):
        rv = ""
        for value in acc.getAsStrCsv().split(","):
            if len(value) > 0:
                value = self.cryptoManager.encrypt(value)
            rv += f"{value},"
        rv = rv.strip(",")
        return rv
#----------------------------------------------------------------------------------------------------------------
    def saveToFile(self,string):
        toSave = string+"\n"
        self.fileRawContentAsList.append(toSave)
        self.dbFile.write(toSave)
        print("Saved in file ", toSave)
#----------------------------------------------------------------------------------------------------------------
    def emptyDbFile(self):
        pathToFile = self.getFileFullPath()
        self.closeFile()
        os.remove(pathToFile)
        self.dbFile = open(file=pathToFile, mode="w+", encoding="ASCII")
#----------------------------------------------------------------------------------------------------------------
    def prepareToResave(self,accSet):
        print(len(self.fileRawContentAsList))
        self.fileRawContentAsList = list(filter(lambda x: Account().setAccountValues(self.decryptLine(x)) not in accSet,self.fileRawContentAsList))
        print(len(self.fileRawContentAsList))
#----------------------------------------------------------------------------------------------------------------
    def removeAccountFromFile(self,acc):
        helpSet = set()
        helpSet.add(acc)
        self.prepareToResave(helpSet)
        self.emptyDbFile()
        self.resaveDB()
#----------------------------------------------------------------------------------------------------------------
    def resaveDB(self):
        print("Zapisuje")
        for line in self.fileRawContentAsList:
            print(Account().setAccountValues(self.decryptLine(line)))
        self.dbFile.writelines(self.fileRawContentAsList)
