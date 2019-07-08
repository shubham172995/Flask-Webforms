from flask import render_template, flash, redirect
from app import app
import smtplib
from app import db
from app.models import User, Post
from app.forms import LoginForm
from app.forms import RegistrationForm, ActivityForm, ConfirmationForm
"""
Script - send gmail from Python code.
Requirement: Gmail user name, password.
1. Create config file which include email password and read that from this script.
"""
# User defined classes and functions
# Configuration file
from config import Credentials
# Utility class to get email content (OTP)
from utility import Utility


# Start - Set
TO = 'ToEmail@gmail.com'    # read from the calling script
SUBJECT = 'TEST MAIL'   # change as per the requirement
BODY_TEXT = Utility.get_email_message() # User defined message per requirement

# Gmail Sign In
gmail_sender = Credentials.email_sender

# Save password in config file and restrict access of file for others.
gmail_passwd = Credentials.GMAIL_PASSWORD

# Start - Email Server Setup
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)
# End - Email Server Setup

# Set email body
BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', BODY_TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print('email sent')
except:
    print('error sending mail')

server.quit()
