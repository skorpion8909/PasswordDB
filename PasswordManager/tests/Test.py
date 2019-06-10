from PasswordManager.PasswordDB import PasswordDB
from PasswordManager.Account import Account


filePath = "testFile.pass"

pwDb = PasswordDB("H2",filePath)             # type: PasswordDB
pwDb.fileManager.emptyDbFile()
acc = Account("name1","login","password1")
pwDb.addAccount(acc)

pwDb.closeDB()

pwDb = PasswordDB("H3",filePath)             # type: PasswordDB

acc = Account("name2","login","password1")
pwDb.addAccount(acc)

pwDb.changeMainPassword("H4")

acc = Account("name1","login","password1")
pwDb.addAccount(acc)

print(len(pwDb.getAccountSet()))
