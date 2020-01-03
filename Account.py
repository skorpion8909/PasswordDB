from PasswordManager.Cipher import Cipher

class Fields:
    """class enum type"""
    NAME = "NAME"
    LOGIN = "LOGIN"
    PASSWORD1 = "PASSWORD1"
    PASSWORD2 = "PASSWORD2"
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

        raise ValueError("Impossibru")
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
#----------------------------------------------------------------------------------------------------------------

