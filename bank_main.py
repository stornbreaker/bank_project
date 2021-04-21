import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)



database_file = "sqlite:///bank.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

@app.route("/", methods = ["GET","POST"])
def log_in():
    return render_template("log_in.html")

@app.route("/log_in_client", methods =["GET","POST"] )
def log_in_client():
    return render_template("log_in_client.html")

@app.route("/log_in_employee", methods =["GET","POST"] )
def log_in_employee():
    print(1234)
    return render_template("log_in_employee.html")

@app.route("/menu_employee", methods =["POST"] )
def menu_employee():
    
    employee_PIN=request.form.get("employee_PIN")
    print(employee_PIN)
    return render_template("menu_employee.html")



if __name__ == "__main__":
    app.run(debug=True)