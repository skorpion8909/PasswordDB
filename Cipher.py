from cryptography.fernet import Fernet, MultiFernet

class Cipher:
    """
        Cipher can be use as an object that represents string
        but in memory is encrypted until being use.

    """
    def __init__(self,string):
        string = string.encode("ASCII")
        self.fernet = Fernet(Fernet.generate_key())
        if len(string) == 0 or string == None:
            self.key = ""
        else:
            self.key = self.fernet.encrypt(string)
#----------------------------------------------------------------------------------------------------------------
    def getDecrypted(self):
        if len(self.key) == 0:
            return ""
        rv = self.fernet.decrypt(self.key)
        rv = rv.decode("ASCII")
        return rv
#----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return self.key
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------