from PasswordManager.Account import Fields, Account, getFieldsList
from PasswordManager.PasswordDB import PasswordDB, LoginFlags

testFilePath = 'testFile.pass'

# init of core class, on init loads saved accounts
# on default file is where main class is
# pathToDbFile= *args can be use to change that
pwDb = PasswordDB("H2",pathToDbFile=testFilePath)   # takes password as argument max 32 chars

# set save to True to allow saving credentials in a file
pwDb.setAutoSave(True)

# creating any account
newAcc = Account("name","login","password1","password2") # second password is optional

# adding account to memory and file
# if identical credentials where provided(e.g. while loading) acc will not be saved
pwDb.addAccount(newAcc)

# a way for getting account object from core object
acc = pwDb.getAccount("name")
print(acc)
# getting decrypted value
print(acc.getDecryptedAttribute(Fields.LOGIN),"<--- login name")

# removing account
pwDb.removeAccount(acc)
# or
newAcc = Account("name","login","password1","password2")
pwDb.addAccount(newAcc)
pwDb.removeAccount("name")


# this will return list of all allowed Fields e.x
print(getFieldsList())
# ['NAME', 'LOGIN', 'PASSWORD1', 'PASSWORD2']

#Flag cases
#pwDb = PasswordDB(flag=LoginFlags.CONSOLE)  #<---- will ask for a password from console
# if you want to test your code in ide you should pass ideEnvironmen=True
# password will be visible in console but it will work.
# in normal use case getpass will be use by default to input password
#pwDb = PasswordDB(flag=LoginFlags.GUI)      #<---- will ask for a password from PyQt5 GUI



