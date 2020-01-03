from PasswordManager.PasswordDB import openAddAccountGUI,PasswordDB

gui = openAddAccountGUI()
password = gui.getPassword()
acc = gui.getAccount()
PasswordDB(password).addAccount(acc)
