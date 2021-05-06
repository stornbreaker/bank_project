import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)


database_file2 = "sqlite:///transactions.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file2

id_tr = 0 



class customer(db.Model):
    accountNumber = db.Column(db.String,nullable=False,primary_key=True)
    firstName = db.Column(db.String,nullable= False)
    lastName = db.Column(db.String,nullable=False)
    currentAccount = db.Column(db.Integer, nullable=False)
    savingAccount = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String,nullable=False)

    def __init__(self,firstName,lastName,accountNumber,email):
        
        self.firstName = firstName
        self.lastName = lastName
        self.accountNumber = accountNumber
        self.email = email
        self.currentAccount = 0
        self.savingAccount = 0


    def __repr__(self):
        return '<customer %s>' % self.accountNumber

    def getPIN(self):
        return self.accountNumber[-5:-3] + self.accountNumber[-2:]


class transaction(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    amount = db.Column(db.Integer,nullable=False)
    customer_Num = db.Column(db.String,nullable = False)
    account = db.Column(db.String,nullable=False)
    

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





@app.route("/", methods = ["GET","POST"])
def log_in():
    return render_template("log_in.html")

@app.route("/log_in_customer", methods =["GET","POST"] )
def log_in_customer():
    return render_template("log_in_customer.html")

@app.route("/log_in_employee", methods =["GET","POST"] )
def log_in_employee():
    return render_template("log_in_employee.html")

@app.route("/menu_employee", methods =["POST"] )
def menu_employee():
    
    employee_PIN=request.form.get("employee_PIN")
    if employee_PIN == "A1234":
        accounts = customer.query.all()
        return render_template("menu_employee.html",accounts= accounts)
    else:
        return render_template ("log_in_employee.html",message = "failed")
    
@app.route("/new_customer", methods = ["POST"])
def newCustomer():
    if request.method == 'POST':
        firstName = request.form['customer_firstName'] 
        lastName = request.form['customer_lastName']
        email = request.form['customer_email']

        accountNum = getNumAcc(firstName, lastName)
        newCos=customer(firstName=firstName,lastName=lastName,accountNumber= accountNum,email=email)
        print(os.path.isfile('%s-%s.txt' % (newCos.accountNumber,'savings')))
        if not os.path.isfile('./customers/%s-%s.txt' % (newCos.accountNumber,'savings')) and not os.path.isfile('./customers/%s-%s.txt' % (newCos.accountNumber,'currents')):
            f = open('./customers/%s-%s.txt' % (newCos.accountNumber,'savings'),'w')
            f.write('%s-%s-%s-%s' % (newCos.accountNumber,newCos.firstName,newCos.lastName,'savings'))
            f.close()
            f = open('./customers/%s-%s.txt' % (newCos.accountNumber,'currents'),'w')
            f.write('%s-%s-%s-%s' % (newCos.accountNumber,newCos.firstName,newCos.lastName,'currents'))
            f.close()

        try :
            db.session.add(newCos)
            db.session.commit()
            accounts = customer.query.all()
            return render_template("menu_employee.html",accounts= accounts)
        except:
            return "there was an issue"
    

    return render_template("new_customer.html")

@app.route("/new_customerPage",methods  =['GET','POST'])
def new_customerPage():
    return render_template("new_customer.html")

@app.route("/delete/<string:accNum>",methods = ['GET','POST'])
def delete(accNum):
    account_to_delete = customer.query.get_or_404(accNum)

    try:
        db.session.delete(account_to_delete)
        for tr in transaction.query.all():
            if tr.customer_Num == account_to_delete.accountNumber:
                db.session.delete(tr)
        db.session.commit()

        os.remove('./customers/%s-%s.txt' % (accNum,'currents'))
        os.remove('./customers/%s-%s.txt' % (accNum,'savings'))
        

        accounts = customer.query.all()
        return render_template("menu_employee.html",accounts= accounts)
    except:
        return "there was a issue"

@app.route("/menu_customer",methods = ['GET','POST'])
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
def description(accNum):
    account= customer.query.get_or_404(accNum)
    currents,savings = [],[]
    for tr in transaction.query.all():
        if tr.customer_Num == accNum:
            if tr.account == "current":
                currents.append([tr.id,tr.amount])
            else:
                savings.append([tr.id,tr.amount])
    

    return render_template("employee_view_customer.html",customer= account,currents= currents,savings = savings)

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
            cust.currentAccount = cust.currentAccount + int(amount)
        else:
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


