import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)


database_file2 = "sqlite:///bank.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file2

id_tr = 0 



class customer(db.Model):
    accountNumber = db.Column(db.String,nullable=False,primary_key=True)
    firstName = db.Column(db.String,nullable= False)
    lastName = db.Column(db.String,nullable=False)
    currentAccount = db.Column(db.Integer, nullable=False)
    savingAccount = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String,nullable=False)

    #we create a class that contain mains informations for a person and the minimum that we need
    # we choosed to not take the PIN as a object of the class because it can be taken in the account number.

    def __init__(self,firstName,lastName,accountNumber,email):
        
        self.firstName = firstName
        self.lastName = lastName
        self.accountNumber = accountNumber
        self.email = email
        self.currentAccount = 0
        self.savingAccount = 0

        #this is the function creating objects of the class

    def __repr__(self):
        return '<customer %s>' % self.accountNumber

    def getPIN(self):
        return self.accountNumber[-5:-3] + self.accountNumber[-2:]
        #this function allow to get the pin code from the account number by getting the numbers associated

class transaction(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    amount = db.Column(db.Integer,nullable=False)
    customer_Num = db.Column(db.String,nullable = False)
    account = db.Column(db.String,nullable=False)
    #here is the class of the transactions where it is defined by an id as the primary key, an amount a customer ans the account of the 
    #customer which will recieved the transaction.  There are all the informations that are needed to get a transactions and each transaction is 
    #recognizable by its id allowing the costumer to get the same amount on the same account many times.

    def __init__(self, id, amount,customer,account):
        self.id = id
        self.amount = amount
        self.customer_Num = customer 
        self.account = account

def getNumAcc(firstName,lastName):
        alphabet="abcdefghijklmonpqrstuvwxyz"
        nombre = range(1,27)
        initials=firstName[0].lower() + lastName[0].lower()

        length = len(firstName) + len(lastName)
        ### find the numbers corresponding
        yy = nombre[alphabet.index(firstName[0].lower())]
        zz = nombre[alphabet.index(lastName[0].lower())]

        return initials + "-"+str(length) + "-" + "%02d-%02d" % (yy,zz)
        #this function allows to create the account number of clients based on their firstname and lastname
        #we create an alphabet to get the place(index) of the initials of names and we concatenate with 
        # others informations we got easily from names




@app.route("/", methods = ["GET","POST"])
def log_in():
    return render_template("log_in.html")
    #this is the first page we can see and the entry to all the other pages. On this page we will be able to choose if he is a customer 
    # or a employee

@app.route("/log_in_customer", methods =["GET","POST"] )
def log_in_customer():
    return render_template("log_in_customer.html")
    #this the function allowing to go to the log in page for customer

@app.route("/log_in_employee", methods =["GET","POST"] )
def log_in_employee():
    return render_template("log_in_employee.html")
    #this code allow also to go to the log in page for employee

@app.route("/menu_employee", methods =["POST"] )
def menu_employee():
    
    employee_PIN=request.form.get("employee_PIN")
    if employee_PIN == "A1234":
        accounts = customer.query.all()
        return render_template("menu_employee.html",accounts= accounts)
    else:
        return render_template ("log_in_employee.html",message = "failed")
    #this function check if the PIN is correct or not and then dirst you to the menu of employee or back to the log in to retry

@app.route("/new_customer", methods = ["POST"])
def newCustomer():
    if request.method == 'POST':
        firstName = request.form['customer_firstName'] 
        lastName = request.form['customer_lastName']
        email = request.form['customer_email']
        #here we recuperate hte informations we will need to add customer like the firstname, the lastname, and the email.
        accountNum = getNumAcc(firstName, lastName)     #it create the account number with the function created for it
        newCos=customer(firstName=firstName,lastName=lastName,accountNumber= accountNum,email=email)  #we create the customer wih all informations
        if not os.path.isfile('./customers/%s-%s.txt' % (newCos.accountNumber,'savings')) and not os.path.isfile('./customers/%s-%s.txt' % (newCos.accountNumber,'currents')):
            f = open('./customers/%s-%s.txt' % (newCos.accountNumber,'savings'),'w')
            f.write('%s-%s-%s-%s' % (newCos.accountNumber,newCos.firstName,newCos.lastName,'savings'))
            f.close()
            f = open('./customers/%s-%s.txt' % (newCos.accountNumber,'currents'),'w')
            f.write('%s-%s-%s-%s' % (newCos.accountNumber,newCos.firstName,newCos.lastName,'currents'))
            f.close()
        else:
            return "there is a problem in the files, some documents are already existing"
        #we verifiy if the files for the customers are not already taken and then it create it 
        try :
            db.session.add(newCos)
            db.session.commit()
            accounts = customer.query.all()
            return render_template("menu_employee.html",accounts= accounts)
            #it finaly add the customer in the database and return to the page of the menu of employee
        except:
            return "there was an issue"
    

    return render_template("new_customer.html")

@app.route("/new_customerPage",methods  =['GET','POST'])
def new_customerPage():
    return render_template("new_customer.html")
    #this function just leed to the page to create a new customer

@app.route("/delete/<string:accNum>",methods = ['GET','POST'])
#this function will delete en account with all that will go with
def delete(accNum):
    account_to_delete = customer.query.get_or_404(accNum)
    #we get the customer associated with the account number tranmite by the route(accNum)
    try:
        db.session.delete(account_to_delete) # we delete the count of the customer we have found
        for tr in transaction.query.all():
            if tr.customer_Num == account_to_delete.accountNumber:
                db.session.delete(tr) # we deleteall the transactions linked with this account in the database of transactions
        db.session.commit()

        os.remove('./customers/%s-%s.txt' % (accNum,'currents'))
        os.remove('./customers/%s-%s.txt' % (accNum,'savings'))
        #then we delete the files of this account

        accounts = customer.query.all()
        return render_template("menu_employee.html",accounts= accounts) #then we go back to the menu of the employee with the list of all accounts
    except:
        return "there was a issue"
    

@app.route("/menu_customer",methods = ['GET','POST'])
#this function will lead to the menu
def menu_customer():
    lastName = request.form['customer_lastName']
    accNum = request.form['customer_accountNumber']
    PIN = request.form['customer_PIN']
    account= customer.query.get_or_404(accNum)
    currents,savings = [],[]
    for tr in transaction.query.all():
        if tr.customer_Num == accNum:
            if tr.account == "current":
                currents.append([tr.id,tr.amount])
            else:
                savings.append([tr.id,tr.amount])
    if lastName == account.lastName and PIN == account.getPIN():
        return render_template("menu_customer.html",customer = account,currents= currents,savings = savings)
    return render_template("log_in_customer.html",message = "not fount try again")

@app.route("/log_out")
def logout():
    return redirect("/")

@app.route("/return_menu_employee",methods = ['POST'])
def return_menue_employee():
    accounts = customer.query.all()
    return render_template("menu_employee.html",accounts= accounts)

@app.route("/description/<string:accNum>",methods = ['GET','POST'])
def description(accNum,message = ''):
    account= customer.query.get_or_404(accNum)
    currents,savings = [],[]
    for tr in transaction.query.all():
        if tr.customer_Num == accNum:
            if tr.account == "current":
                currents.append([tr.id,tr.amount])
            else:
                savings.append([tr.id,tr.amount])
    

    return render_template("employee_view_customer.html",customer= account,currents= currents,savings = savings,message = message)

@app.route("/new_transaction/<string:accNum>/<string:account>",methods = ['GET','POST'])
def new_tr(accNum,account):
    if request.method == 'POST':
        taken_id = [tr.id for tr in transaction.query.all()]
        id = 0
        while (id in taken_id):
            id+=1
        amount = request.form['add_tr']
        new_tr = transaction(id, amount, accNum, account)
        cust = customer.query.get_or_404(accNum)

        f = open('./customers/%s-%ss.txt' % (cust.accountNumber,account),'a')
        f.write('\n%s\t%s\t%s'  % (id,'01-01-01',amount))
        f.close()

        if account =='current':
            if cust.currentAccount + int(amount)< 0:
                return description(accNum,'failed, your current account cannot be under 0')
            cust.currentAccount = cust.currentAccount + int(amount)
        else:
            if cust.savingAccount + int(amount)< 0:
                return description(accNum,'failed, your saving account cannot be under 0')
            cust.savingAccount = cust.savingAccount + int(amount)
        try :
            db.session.add(new_tr)
            db.session.commit()

           
            return redirect("/description/"+accNum)
        except:
            return "there was an issue a"
    else:
        return "there was a issue b"


@app.route("/delete_tr/<string:id>",methods=['GET','POST'])
def delete_tr(id):
    tr = transaction.query.get_or_404(id)
    cust = customer.query.get_or_404(tr.customer_Num)
    
    db.session.delete(tr)
    if tr.account =='current':
        cust.currentAccount = cust.currentAccount - int(tr.amount)
    else:
        cust.savingAccount = cust.savingAccount - int(tr.amount)
    db.session.commit()
    return redirect("/description/"+cust.accountNumber)


if __name__ == "__main__":
    app.run(debug=True)


