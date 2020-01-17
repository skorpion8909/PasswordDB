Encrypted credentials manager
=============================


<span id="anchor"></span>General info
-------------------------------------

This is a simple project that I wrote for myself to have some of my credentials store safely.


<span id="anchor"></span>Simple use case example
---------------------------------------------

Loading saved account, adding new account, getting encrypted field
```
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
# if identical credentials where provided(e.g. while loading) acc will be replaced
pwDb.addAccount(newAcc)

# a way for getting account object from core object
acc = pwDb.getAccount("name")
print(acc)
# getting decrypted value
print(acc.getDecryptedAttribute(Fields.LOGIN),"<--- login name")
# or
print(acc.getLogin())
print(acc.getPassword1())
print(acc.getPassword2())

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
# if you want to test your code in ide you should pass ideEnvironment=True

#pwDb = PasswordDB(flag=LoginFlags.CONSOLE,ideEnvironment=True)
# password will be visible in console but it will work.
# in normal use case getpass will be use by default for input password

#pwDb = PasswordDB(flag=LoginFlags.GUI)      #<---- will ask for a password from PyQt5 GUI
```

<span id="anchor-1"></span>Technologies
---------------------------------------

-    Python 3.7.2
-    cryptography 2.6.1

<span id="anchor-2"></span>Setup
--------------------------------

1.   Clone github repository(PasswordManager folder).
2.   Pip install main encryption lib <https://pypi.org/project/cryptography/>.
3.   Copy cloned folder to your python distribution site-packages folder (Windows example C:\Users\Username\AppData\Local\Programs\Python\Python37\Lib\site-packages)
4.   Use in your scripts as in provided example

<span id="anchor-3"></span>Features
-----------------------------------

-    Store credentials in encrypted form
-    Encrypt credentials in memory

TO-DO list:

-    [X] More tests
-    [X] Delete account function
-    [X] Change login/password function
-    [X] Api for console and GUI password entry
-    [ ] Make Gui more beautiful
-    [ ] Improve safety by double encryption

<span id="anchor-4"></span>Status
---------------------------------

Project is: **in progress**

Author
------

**Adrian Baczyński**

********

LinkedIn: [https://www.linkedin.com/in/adrianbaczynski/](https://www.linkedin.com/in/adrianbaczynski/)

Github: <https://github.com/skorpion8909>