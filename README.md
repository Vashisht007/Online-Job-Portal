
VirtuHire – Resume Submission & Admin Management Portal
========================================================

A Flask-based web application for handling user registration, secure login, OTP verification, resume uploads, and admin management.

Project Structure
-----------------
.
├── edit.py                  # Basic user signup/login system (simplified version)
├── tempCodeRunnerFile.py   # Full-featured main application with admin and OTP functionality
├── web.py                  # Similar to tempCodeRunnerFile.py, serves similar purpose
├── utlis.py                # Utility functions for file validation
├── templates/              # HTML files (not included here)
└── uploads/                # Uploaded resume files (stored in binary in DB)

Features
--------
User Features:
- Signup/Login with password hashing
- OTP verification via email
- Upload resume (PDF, PNG, JPG)
- Store and manage personal and job-related details
- Download uploaded files

Admin Features:
- Admin signup/login
- View all user-submitted details
- Download user resumes
- Send interview call emails via SMTP

Getting Started
---------------
Prerequisites:
- Python 3.8+
- MySQL server with database `register`
- Gmail account for SMTP

Installation:
1. Clone the repo and navigate to directory.
2. Install dependencies:
   pip install -r requirements.txt

requirements.txt sample:
------------------------
Flask
Flask-Login
Flask-Mail
Flask-WTF
Flask-SQLAlchemy
Werkzeug
email-validator
pyotp

MySQL Setup:
------------
Ensure your DB URI matches in `.py` files:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3307/register'

Email Setup:
------------
Use Gmail SMTP with app passwords:
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

Running the App:
----------------
python tempCodeRunnerFile.py

Open: http://localhost:5000

Route Summary:
--------------
/                - Login page
/signup          - Register user
/verify          - Send OTP
/validate        - OTP check
/details         - User job/resume submission
/download/<file> - Download resumes
/adminsignup     - Admin register
/adminlogin      - Admin login
/ain             - Admin view all
/admind/<email>  - View user details
/sendmail/<email> - Email job notification

Author
Vashisht Urgonda
------
VirtuHire - For HR screening and resume management.
