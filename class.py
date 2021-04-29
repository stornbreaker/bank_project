class Person(db.Model):
    __init__(self,firstName,lastName,accountNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.accountNumber = accountNumber

class Client(Person):
    __init__(self,firstName,lastName,accountNumber,savingAccount,currentAccount):
        self.firstName = firstName
        self.lastName = lastName
        self.accountNumber = accountNumber
        self.savingAccount = savingAccount
        self.currentAccount = currentAccount

class Employee(Person):
    __init__(self,firstName,lastName,accountNumber)
