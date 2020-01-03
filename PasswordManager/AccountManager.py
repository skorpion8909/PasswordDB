from PasswordManager.Account import Account,Fields
from cryptography.fernet import InvalidToken

class AccountManager:
    """This class manages all account in file and memory"""
    def __init__(self,fileManager):
        self.autoSave = False
        self.accountSet = set()
        self.fileManager = fileManager    # type: FileManager

    def loadAccount(self,dataAsList):
        count = 0
        for row in dataAsList:
            count += 1
            if "InvalidToken" in str(row):
                print(f"Account on row num {count} encrypted with different password")
                continue
            if not isinstance(row,list) or not isinstance(row,tuple):
                row = row.split(",")
                row = list(filter(lambda x: True if len(x) > 0 else False,row))

            correctValue = 4
            if len(row) > correctValue:
                print(f"Account at row {count} could not be added added")
                print(f"Amount of parameters wrong")
                size = len(row)
                print(f"Should be {correctValue} is {size}")
                continue

            # adding empty space for avoiding index range error
            [row.append("") for x in range(0,4-len(row))]
            acc = Account(row[0],row[1],row[2],row[3])
            self.accountSet.add(acc)
        size = len(self.accountSet)
        if size > 0:
            print("All current manage accounts ->",[x.getDecryptedAttribute(Fields.NAME) for x in self.accountSet])
        print("Num of accounts loaded ->", size)
#----------------------------------------------------------------------------------------------------------------
    def getNumOfAccount(self):
        return len(self.accountSet)
#----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return f"Number of accounts is {self.getNumOfAccount()}"
#----------------------------------------------------------------------------------------------------------------
    def getSetAccounts(self):
        return self.accountSet
#----------------------------------------------------------------------------------------------------------------
    def addAccount(self,accountObj):
        readBefore = len(self.accountSet)
        if accountObj in self.accountSet:
            print("Removing old acc with that name and saving a new one")
            self.removeAccount(accountObj)
        self.accountSet.add(accountObj)

        if len(self.accountSet) != readBefore and self.autoSave == True:
            self.fileManager.saveAccount(accountObj)
#----------------------------------------------------------------------------------------------------------------
    def setAutoSave(self, boolValue):
        self.autoSave = boolValue
#----------------------------------------------------------------------------------------------------------------
    def getAccountByName(self, accountName):
        for acc in self.accountSet:
            if acc.getDecryptedAttribute(Fields.NAME) == accountName:
                return acc
        return None
#----------------------------------------------------------------------------------------------------------------
    def resaveAccounts(self,password):
        for account in self.accountSet:
            self.fileManager.saveAccount(account)
        print("Accounts resaved")
#----------------------------------------------------------------------------------------------------------------
    def removeAccount(self,acc):
        if isinstance(acc,str):
            acc = self.getAccountByName(acc)
        if acc in self.accountSet:
            self.accountSet.remove(acc)
            self.fileManager.removeAccountFromFile(acc)
        else:
            print("Account not found")