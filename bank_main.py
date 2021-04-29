import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


    
class customer(db.Model):
    accountNumber = db.Column(db.String,nullable=False,primary_key=True)
    firstName = db.Column(db.String,nullable= False)
    lastName = db.Column(db.String,nullable=False)
    #currentAccount = db.Column(db.Integer, nullable=False)
    #savingAccount = db.Column(db.Integer, nullable=False)

    def __init__(self,firstName,lastName,accountNumber):
        
        self.firstName = firstName
        self.lastName = lastName
        self.accountNumber = accountNumber



    def __repr__(self):
        return '<customer %s>' % self.accountNumber

    def getPIN(self):
        return self.accountNumber[-5:-3] + self.accountNumber[-2:]

    def getNum(self):
        alphabet="abcdefghijklmonpqrstuvwxyz"
        nombre = range(1,27)
        initials=self.firstName[0].lower() + self.lastName[0].lower()

        length = len(self.firstName) + len(self.lastName)
        ### find the numbers corresponding
        yy = nombre[alphabet.index(self.firstName[0].lower())]
        zz = nombre[alphabet.index(self.lastName[0].lower())]

        return initials + "-"+str(length) + "-" + "%02d-%02d" % (yy,zz)



database_file = "sqlite:///bank.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

@app.route("/", methods = ["GET","POST"])
def log_in():
    return render_template("log_in.html")

@app.route("/log_in_customer", methods =["GET","POST"] )
def log_in_customer():
    return render_template("log_in_customer.html")

@app.route("/log_in_employee", methods =["GET","POST"] )
def log_in_employee():
    print(1234)
    return render_template("log_in_employee.html")

@app.route("/menu_employee", methods =["POST"] )
def menu_employee():
    
    employee_PIN=request.form.get("employee_PIN")
    print(employee_PIN)
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
        

        accountNum = request.form['customer_accountNumber']
        newCos=customer(firstName=firstName,lastName=lastName,accountNumber= accountNum)


        
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
        db.session.commit()
        accounts = customer.query.all()
        return render_template("menu_employee.html",accounts= accounts)
    except:
        return "there was a issue"

@app.route("/menu_customer",methods = ['GET','POST'])
def menuCustomer():
    lastName = request.form['customer_lastName']
    accountNum = request.form['customer_accountNumber']
    PIN = request.form['customer_PIN']
    account_customer = customer.query.get_or_404(accountNum)
    if lastName == account_customer.lastName and PIN == account_customer.getPIN():
        return render_template("/menu_customer.html",customer = account_customer)
    return render_template("log_in_customer.html",message = "not fount try again")






if __name__ == "__main__":
    app.run(debug=True)


