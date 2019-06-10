import random
import base64
from itertools import cycle
from PasswordManager.OtherMethods import install
from PasswordManager.Cipher import Cipher

try:
    from cryptography.fernet import Fernet, MultiFernet
except Exception:
    print('You need "cryptography" lib')
    print("Trying to install")
    install("cryptography")
    print("Installation completed")
    from cryptography.fernet import Fernet, MultiFernet

class CryptoManager:
    def __init__(self,mainPassword=None):
        """
        This class takes care of encryption layer
        :param mainPassword: <--- password from user, len() can't be 0
        """
        # check for a correct type and value
        if not mainPassword == None:
            self.mainPw = Cipher(self.checkAndGeneratePassword(mainPassword))
        else:
            # self.pw = "".join([chr(random.randrange(33, 126)) for x in range(1, 33)]) # 32 is "space" in ascii 126 is list char ~
            self.mainPw = Cipher(Fernet.generate_key())

        key = bytes(self.mainPw.getDecrypted().encode("ASCII"))

        # init main math logic module
        self.f = Fernet(base64.urlsafe_b64encode(key))
#----------------------------------------------------------------------------------------------------------------
    def generateKey(self,string):
        """Extends value to 32 len() str """
        index = 0
        rv = ""
        iter = cycle(string)
        key = string[0:]
        increment = 1
        # generate a 32 size string
        while len(rv) != 32:
            nextValue = next(iter)
            amount = (ord(key[index])) + increment
            if (index + increment) > 126:
                amount = 126
            rv += nextValue + chr(amount)

            if index + increment >= len(key):
                key = str(rv)
                index = 1
                increment += 1

            index += increment
        else:
            return rv
        return rv
#----------------------------------------------------------------------------------------------------------------
    def checkAndGeneratePassword(self,mainPassword):
        assert isinstance(mainPassword, str), f"mainPassword value must be a str type got {type(mainPassword)}"
        assert len(mainPassword) != 0 and len(
            mainPassword) <= 32 or None, f"len of a string not int range 0<x<33 x int type provided {len(mainPassword)}"

        return self.generateKey(mainPassword)
#----------------------------------------------------------------------------------------------------------------
    def encrypt(self,valueOrObject):
        """Encrypt given string based on a initial key, return it"""
        value = str(valueOrObject)
        self.mainPw.getDecrypted()
        encryptedValue = self.f.encrypt(bytes(value,encoding="UTF-8"))

        return str(encryptedValue)[2:-1] # remove b' and ' before return
#----------------------------------------------------------------------------------------------------------------
    def decrypt(self, valueOrObject):
        """Decrypt given string based on a initial key, return it"""
        value = str(valueOrObject)

        assert isinstance(valueOrObject, str), f"valueOrObject value must be a str type got {type(valueOrObject)}"
        assert len(valueOrObject) != 0, f"len of a string must be bigger then 0"
        decryptedValue = self.f.decrypt(bytes(value, encoding="UTF-8"))
        return str(decryptedValue)[2:-1]

#----------------------------------------------------------------------------------------------------------------
    def decryptLine(self,line):
        print(line)
        toReturn = ""
        try:
            for element in line.split(","):
                toReturn += self.decrypt(element)+","
            toReturn = toReturn.strip(",")
        except Exception:
            return ""
        return toReturn
#----------------------------------------------------------------------------------------------------------------
    def changePassword(self,newPassword):
        self.mainPw = Cipher(self.checkAndGeneratePassword(newPassword))
        key = bytes(self.mainPw.getDecrypted().encode("ASCII"))
        # init main math logic module
        self.f = Fernet(base64.urlsafe_b64encode(key))
#----------------------------------------------------------------------------------------------------------------
