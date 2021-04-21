import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("/", methods = ["GET","POST"])
def log_in():
    return render_template("log_in.html")

@app.route("/log_in_client", methods =["GET","POST"] )
def log_in_client():
    return render_template("log_in_client.html")

@app.route("/log_in_employee", methods =["GET","POST"] )
def log_in_employee():
    return render_template("log_in_employee.html")


if __name__ == "__main__":
    app.run(debug=True)