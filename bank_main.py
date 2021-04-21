import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

@app.route("/", methods = ["GET","POST"])
def log_in():
    if request.form:
        try:
            