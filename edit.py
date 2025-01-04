from flask import Flask, redirect, render_template,flash,request
from flask.globals import request,session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from sqlalchemy import text
from flask_mail import Mail,Message
import smtplib
from email.message import EmailMessage
import json
import smtplib


# mydatabase
local_server = True
app = Flask(__name__)
app.secret_key = "Its Personal"






#this is for getting the unique access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/register'
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(email):
    return User.query.get(int(email))

class Test(db.Model):
    phoneno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))  # Corrected import statement
    password = db.Column(db.String(20))
class User(UserMixin,db.Model):
    phoneno=db.Column(db.Integer, primary_key=True)
    password=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(20))

# @app.route("/")
# def home():
#     return render_template("index.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        phoneno=request.form.get('phoneno')
       
        # print(email,password,phoneno)
        
        password=User.query.filter_by(password=password).first()
        email=User.query.filter_by(email=email).first()
        # phoneno=User.query.filter_by(phoneno=phoneno).first()
        if email:
            flash("Email already Exists","warning")
            return render_template("signup.html")
        # new_user=db.engine.execute(f"INSERT INTO user (email,password,phoneno) VALUES ('{email}','{password}') ")
        new_user=User(password=password,email=email,phoneno=phoneno)
        db.session.add(new_user)
        db.session.commit()
                
        flash("Sign up successful. Please login.", "success")
        return render_template("index.html")

    return render_template("signup.html")
@app.route("/test")
def test(): 
    try:
        a = Test.query.all()
        print(a)
        return 'My Database is connected'
    except Exception as e:
        print(e)
        return 'My Database is not connected'
    
@app.route('/',methods=['POST','GET'])
def login():
    if request.method=="POST":
        password=request.form.get('password')
        print(f'password: {password}')
        user=User.query.filter_by(password=password).first()
        if user and (user.password==password):
            login_user(user)
            flash("Login Success","info")
            return render_template("signup.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("index.html")


    return render_template("index.html")

app.run(debug=True)