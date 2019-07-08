from flask import render_template, flash, redirect
from app import app
from app import db
from app.models import User, Post
from app.forms import LoginForm
from app.forms import RegistrationForm, ActivityForm, ConfirmationForm
import smtplib
# User defined classes and functions
# Configuration file
from config import Credentials
# Utility class to get email content (OTP)
#from utility import Utility

@app.route('/login', methods=['GET', 'POST'])

def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember me={}'.format(
            form.username.data, form.remember_me.data
        ))
        users=User.query.all()
        for u in users:
            if(u.username==form.username.data):
                if(u.password_hash==form.password.data):
                    flash('Login for user {} successful!!!!'.format(form.username.data))
                    break
    return render_template('login.html', title='Sign in', form = form)

@app.route('/index', methods=['GET', 'POST'])

def index():
    string = "Hey, There. This is first Flask application. This is index1.html"
    user = {'username': 'Shubham'}
    posts = [
        {
            'author': {'username': 'Puneet'},
            'body': 'Beautiful day in Gurgaon'
        },
        {
            'author': {'username': 'Ramakant'},
            'body': 'I am frustrated but this is normal....'
        }
    ]
    return render_template('index3.html', title='Home', str=string, user=user, posts=posts)


@app.route('/register', methods=['GET', 'POST'])

def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash('Registration requested for user {}, Employee Code={}'.format(
            form.username.data, form.employeecode.data
        ))
        u = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, phoneno=form.phoneno.data, employeecode=form.employeecode.data, password_hash=form.password.data)

        # Start - Set
        TO = form.email.data  # read from the calling script
        SUBJECT = 'Confirmation MAIL'  # change as per the requirement
        BODY_TEXT = 'We have a new registration with this EMail ID.'  # User defined message per requirement

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

        db.session.add(u)
        db.session.commit()
    return render_template('register.html', title='Register', form=form)

@app.route('/ayeregister', methods=['GET', 'POST'])

def ayeregister():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash('Registration requested for Customer {}, Employee Code={}'.format(
            form.username.data, form.employeecode.data
        ))
        u = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, phoneno=form.phoneno.data, employeecode=form.employeecode.data, password_hash=form.password.data)

        # Start - Set
        TO = form.email.data  # read from the calling script
        SUBJECT = 'Confirmation MAIL'  # change as per the requirement
        BODY_TEXT = 'We have a new registration with this EMail ID.'  # User defined message per requirement

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

        db.session.add(u)
        db.session.commit()
    return render_template('ayeregister.html', form=form)

@app.route('/ayelogin', methods=['GET', 'POST'])

def ayelogin():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login requested for Aye Employee user {}, remember me={}'.format(
            form.username.data, form.remember_me.data
        ))
        users=User.query.all()
        for u in users:
            if(u.username==form.username.data):
                if(u.password_hash==form.password.data):
                    flash('Login for user {} successful!!!!'.format(form.username.data))
                    break
    return render_template('ayelogin.html', form = form)

@app.route('/ayehome', methods=['GET', 'POST'])

def ayeindex():
    return render_template('ayehome.html', title='Aye Home')

@app.route('/activitychecker', methods=['GET', 'POST'])

def activitychecker():
    form = ActivityForm()
    if form.validate_on_submit():
        users = User.query.all()
        for u in users:
            if(u.username==form.username.data):
                if(u.email==form.email.data):
                    flash('Activity for user {} changed to {}!!!!'.format(form.username.data, form.activity.data))
                    break
    return render_template('activitychecker.html', title='Aye Home', form=form)

@app.route('/confirm', methods=['GET', 'POST'])

def confirmation():
    form=ConfirmationForm()
    if form.validate_on_submit():
        flash('OTP for user {} submitted is {}!!!!'.format(form.username.data, form.otp.data))
    return render_template('confirm.html', form=form)
