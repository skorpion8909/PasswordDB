from PasswordManager.Cipher import Cipher

class Fields:
    """class enum type"""
    NAME = "NAME"
    LOGIN = "LOGIN"
    PASSWORD1 = "PASSWORD1"
    PASSWORD2 = "PASSWORD2"
    @staticmethod
    def getFromNum(num):
        if num == 0:
            return Fields.NAME
        elif num == 1:
            return Fields.LOGIN
        elif num == 2:
            return Fields.PASSWORD1
        elif num == 3:
            return Fields.PASSWORD2
#----------------------------------------------------------------------------------------------------------------
def getFieldsList():
    rv = list()
    for name in Fields().__dir__():
        if name.isupper():
            rv.append(name)
    return rv
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
class Account:
    def __init__(self,name="",login="",password1="",password2=""):
        self.name = Cipher(name)
        self.login = Cipher(login)
        self.password1 = Cipher(password1)
        self.password2 = Cipher(password2)
#----------------------------------------------------------------------------------------------------------------
    def getName(self):
        return self.name.getDecrypted()
#----------------------------------------------------------------------------------------------------------------
    def getLogin(self):
        return self.login.getDecrypted()
#----------------------------------------------------------------------------------------------------------------
    def getPassword1(self):
        return self.password1.getDecrypted()
#----------------------------------------------------------------------------------------------------------------
    def getPassword2(self):
        return self.password2.getDecrypted()
#----------------------------------------------------------------------------------------------------------------
    def getValuesAsList(self):
        return [self.name.getDecrypted(),self.login,self.password1,self.password2]
#----------------------------------------------------------------------------------------------------------------
    def getValueByField(self,field):
        if field == Fields.NAME:
            return self.name.getDecrypted()
        elif field == Fields.LOGIN:
            return self.login.getDecrypted()
        elif field == Fields.PASSWORD1:
            return self.password1.getDecrypted()
        elif field == Fields.PASSWORD2:
            return self.password2.getDecrypted()
#----------------------------------------------------------------------------------------------------------------
    def changeAccountFieldValue(self,field,value):
        if field == Fields.NAME:
            self.name = Cipher(value)
        elif field == Fields.LOGIN:
            self.login = Cipher(value)
        elif field == Fields.PASSWORD1:
            self.password1 = Cipher(value)
        elif field == Fields.PASSWORD2:
            self.password2 = Cipher(value)
        print(self)
#----------------------------------------------------------------------------------------------------------------
    def getAsStrCsv(self):
        n = self.name.getDecrypted()
        l = self.login.getDecrypted()
        p1 = self.password1.getDecrypted()
        p2 = self.password2.getDecrypted()

        return f"{n},{l},{p1},{p2}"
#----------------------------------------------------------------------------------------------------------------
    def getDecryptedAttribute(self,attributeValue):
        if Fields.NAME == attributeValue:
            return self.name.getDecrypted()
        elif Fields.LOGIN == attributeValue:
            return self.login.getDecrypted()
        elif Fields.PASSWORD1 == attributeValue:
            return self.password1.getDecrypted()
        elif Fields.PASSWORD2 == attributeValue:
            return self.password2.getDecrypted()

        raise ValueError("Impossibru, filed does not exist.")
#----------------------------------------------------------------------------------------------------------------
    def setAccountValues(self,csvLine):
        csvLine = str(csvLine)
        splited = csvLine.split(",")
        try:
            self.name = Cipher(splited[0])
        except Exception:
            self.name = Cipher("")
            
        try:
            self.login = Cipher(splited[1])
        except Exception:
            self.login = Cipher("")
            
        try:
            self.password1 = Cipher(splited[2])
        except Exception:
            self.password1 = Cipher("")
            
        try:
            self.password2 = Cipher(splited[3])
        except Exception:
            self.password2 = Cipher("")
        return self
#----------------------------------------------------------------------------------------------------------------
    def __hash__(self):
        """Implement custom __hash__ method"""
        strVal = self.name.getDecrypted()
        hashValue = sum([ord(char) for char in strVal])
        return hash(hashValue)
#----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other):
        if other == None:
            return False

        if self.name.getDecrypted().__hash__() == other.name.getDecrypted().__hash__():
            return True
        else:
            return False
#----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        rv = self.name.getDecrypted()
        return str(rv)
#----------------------------------------------------------------------------------------------------------------
    def __copy__(self):
        return Account(self.name.getDecrypted(), self.login.getDecrypted(), self.password1.getDecrypted(), self.password2.getDecrypted())
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

