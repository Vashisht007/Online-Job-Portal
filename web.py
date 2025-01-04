from flask import Flask, redirect, render_template,flash,request,send_file
from flask.globals import request,session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from sqlalchemy import text
from flask_mail import Mail
from flask_mailman import EmailMessage
import smtplib
from email.message import EmailMessage
import json
import smtplib
from flask import abort
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_session import Session
from io import BytesIO
import pyotp
from random import *
import os


# mydatabase
local_server = True
app = Flask(__name__)
app.secret_key = "Its Personal"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME'] = 'vituehire24@gmail.com'
app.config['MAIL_PASSWORD'] = '@bcd^&*ef'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)






#this is for getting the unique access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3307/register'
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_email):
    return User.query.get(user_email)

class Test(db.Model):
    dob = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))  # Corrected import statement
    password = db.Column(db.String(20))

class User(UserMixin,db.Model):
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(1000))
    dob=db.Column(db.Integer,primary_key=True)

class Adminuser(UserMixin,db.Model):
    admin_email=db.Column(db.String(200),unique=True,nullable=False)
    admin_password=db.Column(db.String(1000))
    admin_phoneno=db.Column(db.Integer,primary_key=True)    
    admin_designation=db.Column(db.String(200))
    admin_companyname=db.Column(db.String(200))
class Details(UserMixin,db.Model):
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    demail = db.Column(db.String(100),unique = True, nullable=False)
    lastjobdesignation = db.Column(db.String(100), nullable=False)
    lastcompany = db.Column(db.String(100), nullable=False)
    ddob= db.Column(db.String(100),primary_key = True,nullable=False)
    address = db.Column(db.String(200), nullable=False)
    domain=db.Column(db.String(10), nullable=False)
    phoneno = db.Column(db.Integer, nullable=False) 
    salary=db.Column(db.BIGINT, nullable=False)
    
class Upload(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    demail = db.Column(db.String(100), nullable=False)
    filename=db.Column(db.String(100))
    data=db.Column(db.LargeBinary)

otp = None

# @app.route("/")
# def home():
#     return render_template("login.html")

secret_key = pyotp.random_base32()

# Initialize a TOTP object
totp = pyotp.TOTP(secret_key)

@app.route('/verify',methods=['GET','POST'])
def verify():
    global otp
    global email1
    otp=randint(000000,999999)
    if request.method == 'POST':
            email1=request.form.get('email')
            # print(email)
            msg = EmailMessage()
            msg.set_content(f'Your OTP is: {otp}')
            msg['Subject'] = "OTP"
            msg['From'] = 'virtuhire042@gmail.com'
            msg['To'] = email1

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('virtuhire042@gmail.com', 'nnwi rdie kpzp tzel')  # Replace with your email and password
                server.send_message(msg)
                server.quit()
                return render_template("otp.html")
            except Exception as e:
                return f"Error: {e}"
    return render_template("forgot.html")        
@app.route('/validate',methods=['POST','GET'])
def validate():
    global otp
    global email1
    user_otp = request.form['otp']
    # Retrieve user's OTP input
    
    
    if otp is not None and otp == int(user_otp):
        return render_template('userindex.html')
    # If the OTP does not match, return 'Wrong'
    return 'Wrong'


@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')

# @app.route('/forgot',methods=['POST','GET'])
# def forgot():
#     return render_template("forgot.html")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        email=request.form.get('email')
        dob=request.form.get('dob')
        password=request.form.get('password')
        enc=generate_password_hash(password) 
       
        #print(email,password,dob)
        
        # password1=User.query.filter_by(password=password).first()
        try :
            existing_email = User.query.filter_by(email=email).first() 
            # # dob=User.query.filter_by(dob=dob).first()
            # print(existing_email.email)
            # if existing_email.email:
            #     flash("Email already exists", "warning")
            #     return render_template("signup.html")
            # # # new_user=db.engine.execute(f"INSERT INTO 'user' ('email','enc','dob') VALUES ('{email}','{enc}','{dob}') ")
            new_user=User(email=email,password=enc,dob=dob)
            # return 'User Added'
            db.session.add(new_user)
            db.session.commit()        
            flash("Sign up successful. Please login.", "success")
            return render_template("login.html")
        except :
            flash("Email Already Exists","Warning")
            return render_template("signup.html")
            # return redirect("signup.html")
            # return render_template("signup.html")      
        # # dob=User.query.filter_by(dob=dob).first()
        # print(existing_email)
        # if existing_email:
        #     flash("Email already exists", "warning")
        #     return render_template("signup.html")

        # # # new_user=db.engine.execute(f"INSERT INTO 'user' ('email','enc','dob') VALUES ('{email}','{enc}','{dob}') ")
        # new_user=User(email=email,password=enc,dob=dob)
        # # return 'User Added'
        # db.session.add(new_user)
        # db.session.commit()        
        # flash("Sign up successful. Please login.", "success")
        # return render_template("login.html")

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

@app.route('/adminsignup',methods=['POST','GET'])
def adminsignup():
    global admin_password
    if request.method=="POST":
        admin_email=request.form.get('admin_email')
        admin_designation=request.form.get('admin_designation')
        admin_password=request.form.get('admin_password')
        admin_enc=generate_password_hash(admin_password)
        admin_companyname=request.form.get('admin_companyname')
        admin_phoneno=request.form.get('admin_phoneno')
        # print(admin_email,admin_dob)
        
        existing_email = Adminuser.query.filter_by(admin_email=admin_email).first() 
        if existing_email:
            flash("Email Already Exists","Warning")
            return render_template("adminsignup.html")
        else:
            new_user=Adminuser(admin_email=admin_email,admin_password=admin_enc,admin_designation=admin_designation,admin_companyname=admin_companyname,admin_phoneno=admin_phoneno)
            # return 'User Added'
            db.session.add(new_user)
            db.session.commit()        
            flash("Sign up successful. Please login.", "success")
            return render_template("adminlogin.html")
        
            
    return render_template("adminsignup.html")             

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    # print("Added")
    global admin_user
    if request.method=="POST":
        admin_email=request.form.get('admin_email')
        admin_password=request.form.get('admin_password')
        session['user']=None
        # print(admin_email)
        # print(f'password: {password}')
        admin_user=Adminuser.query.filter_by(admin_email=admin_email).first()
        # print(admin_user.admin_password)
        if admin_user.admin_email and check_password_hash(admin_user.admin_password,admin_password):
            # login_user(user)
            flash("Sucessfully Logged in","Sucess")
            return render_template("adminindex.html")
        else: 
            flash("Invalid","Warning")
            return render_template("adminlogin.html")


    return render_template("adminlogin.html")



@app.route('/details', methods=['POST', 'GET'])
def dashboard():
 # Create form instance

    if request.method == "POST":
        # Fetch form data
        firstName = request.form.get('firstName')
        demail = request.form.get('demail')
        ddob = request.form.get('ddob')
        lastName = request.form.get('lastName')
        lastjobdesignation = request.form.get('lastjobdesignation')
        lastcompany = request.form.get('lastcompany')
        address = request.form.get('address')
        phoneno = request.form.get('phoneno')
        domain = request.form.get('domain')
        salary = request.form.get('salary')
        file=request.files['file'] 

        
        # db.session.add(upload)
        
        email=Details.query.filter_by(demail=demail).first()
        # name=Details.query.filter_by(name=firstName).first()
        if email:
            flash("  ")
        else:
            # Create a new Details object and add it to the database
            new_det=Details(firstName=firstName,demail=demail,ddob=ddob,lastName=lastName,lastjobdesignation=lastjobdesignation,lastcompany=lastcompany,address=address,phoneno=phoneno,domain=domain,salary=salary)
            db.session.add(new_det)
            db.session.commit()
            dict = {"demail":new_det.demail,"firstName":new_det.firstName,"lastName":new_det.lastName,"ddob":new_det.ddob,"lastjobdesignation":new_det.lastjobdesignation,"lastcompany":new_det.lastcompany,"domain":new_det.domain,"phoneno":new_det.phoneno,"address":new_det.address,"salary":new_det.salary}
            session['user'] = dict
        
        
        upload= Upload(filename=file.filename , data=file.read(),demail=demail)
        db.session.add(upload)
        db.session.commit()
        # if upload:
        #     return render_template("userdetails.html")
        

        # return f'Uploaded:{file.filename}'
        

    return render_template("userdetails.html",user=User)     
        
@app.route('/download/<filename>')
def download_file(filename):
    file_data = Upload.query.filter_by(filename=filename).first()
    return send_file(BytesIO(file_data.data), download_name=filename, as_attachment=True)        
    
@app.route('/')
def home():
    return render_template("index.html")     

@app.route('/uindex')
def uindex():
    return render_template("userindex.html") 

@app.route('/aindex')
def aindex():
    return render_template("adminindex.html") 

@app.route('/admind/<aperson>',methods=['GET','POST'])
def admind(aperson):

    # upload=Upload.query.filter_by(id=upload_id).first()
    # a = send_file(BytesIO(upload.data),attachment_filename=upload.filename)
    down=Upload.query.filter_by(demail=aperson).first()
    person =Details.query.filter_by(demail=aperson).first()
    dict = {"demail":person.demail,"firstName":person.firstName,"lastName":person.lastName,"ddob":person.ddob,"lastjobdesignation":person.lastjobdesignation,"lastcompany":person.lastcompany,"domain":person.domain,"phoneno":person.phoneno,"address":person.address,"salary":person.salary,"filename":down.filename}
    # print(dict)
    return render_template("Admind.html",aperson = dict)
    # return render_template("admind.html",aperson = aperson)



@app.route('/sendmail/<email>', methods=['POST', 'GET'])
def send_mail(email):
    if request.method == 'POST':
        if 'accept' in request.form:
            print(email)
            msg = EmailMessage()
            msg.set_content("Dear Candidate,\nYou Have Been Selected for the Interview At [CompanyName]\nYou will shortly get the details about the Interview")
            msg['Subject'] = " Invitation to Interview at [Company Name]"
            msg['From'] = 'virtuhire042@gmail.com'
            msg['To'] = email

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('virtuhire042@gmail.com', 'nnwi rdie kpzp tzel')  # Replace with your email and password
                server.send_message(msg)
                server.quit()
                return 'Email Has Been Sent Go Back To The Job Page'
                
            except Exception as e:
                return f"Error: {e}"
    return render_template('a.html')



@app.route('/ain',methods=['POST', 'GET'])
def ain():
    all=Details.query.all()
    return render_template("a.html",all=all) 

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        det = Details.query.filter_by(demail=email).first()

        if user:
            if check_password_hash(user.password, password):
                
                if det:
                    dict = {
                        "demail": det.demail,
                        "firstName": det.firstName,
                        "lastName": det.lastName,
                        "ddob": det.ddob,
                        "lastjobdesignation": det.lastjobdesignation,
                        "lastcompany": det.lastcompany,
                        "domain": det.domain,
                        "phoneno": det.phoneno,
                        "address": det.address,
                        "salary": det.salary
                    }
                    session['user'] = dict
                return render_template("userindex.html")
            else:
                flash("Invalid password", "warning")
                return render_template("login.html")
        else:
            flash("Invalid email", "warning")
            return render_template("login.html")

    return render_template("login.html")

app.run(debug=True)