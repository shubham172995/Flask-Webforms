from flask import render_template, flash, redirect, url_for, request
from app import app
from werkzeug.urls import url_parse
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm
from app.forms import RegistrationForm, ActivityForm, ConfirmationForm
import smtplib
import random
# User defined classes and functions
# Configuration file
from config import Credentials
# Utility class to get email content (OTP)
#from utility import Utility

@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = VerifiedUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])

def index():
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
    return render_template('index3.html', title='Home', posts=posts)


@app.route('/register', methods=['GET', 'POST'])

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        temp = User.query.filter_by(username=form.username.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this username already exists')
            return render_template('register.html', form=form)
        temp = form.phoneno.data
        if(len(temp)!=10):
            flash('Invalid Phone Number. Enter a valid 10 digit Phone Number.')
            return render_template('register.html', form=form)
        if(not temp.isnumeric()):
            flash('Invalid Phone Number. Only Digits allowed')
            return render_template('register.html', form=form)
        temp=User.query.filter_by(phoneno=form.phoneno.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this Phone Number already exists')
            return render_template('register.html', form=form)
        temp = User.query.filter_by(email=form.email.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this username already exists')
            return render_template('register.html', form=form)
        temp = User.query.filter_by(employeecode=form.employeecode.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this employee code already exists')
            return render_template('register.html', form=form)
        flash('Registration requested for user {}, Employee Code={}'.format(
            form.username.data, form.employeecode.data
        ))
        u = User(email=form.email.data, username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, phoneno=form.phoneno.data, employeecode=form.employeecode.data, password_hash=form.password.data, otp=random.randint(1000, 9999))
        db.session.add(u)
        db.session.commit()
        # Start - Set
        TO = form.email.data  # read from the calling script
        SUBJECT = 'Confirmation MAIL'  # change as per the requirement
        BODY_TEXT = 'We have a new registration with this EMail ID. The OTP is {}'.format(u.otp)  # User defined message per requirement

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
        return redirect('/confirm')
    return render_template('register.html', form=form)


@app.route('/ayeregister', methods=['GET', 'POST'])

def ayeregister():
    form=RegistrationForm()
    if form.validate_on_submit():
        temp = User.query.filter_by(username=form.username.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this username already exists')
            return render_template('register.html', form=form)
        temp = form.phoneno.data
        if (len(temp) != 10):
            flash('Invalid Phone Number. Enter a valid 10 digit Phone Number.')
            return render_template('register.html', form=form)
        if (not temp.isnumeric()):
            flash('Invalid Phone Number. Only Digits allowed')
            return render_template('register.html', form=form)
        temp = User.query.filter_by(phoneno=form.phoneno.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this Phone Number already exists')
            return render_template('register.html', form=form)
        temp = User.query.filter_by(email=form.email.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this username already exists')
            return render_template('register.html', form=form)
        temp = User.query.filter_by(employeecode=form.employeecode.data).first()
        if (temp):
            flash('Invalid User Credentials. User with this employee code already exists')
            return render_template('register.html', form=form)
        flash('Registration requested for Customer {}, Employee Code={}'.format(
            form.username.data, form.employeecode.data
        ))
        u = User(otp=random.randint(1000, 9999), username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, phoneno=form.phoneno.data, employeecode=form.employeecode.data, password_hash=form.password.data, email=form.email.data)
        db.session.add(u)
        db.session.commit()
        # Start - Set
        TO = form.email.data  # read from the calling script
        SUBJECT = 'Confirmation MAIL'  # change as per the requirement
        BODY_TEXT = 'We have a new registration with this EMail ID.The OTP is {}'.format(u.otp)  # User defined message per requirement

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
        return redirect('/confirm')
    return render_template('ayeregister.html', form=form)

@app.route('/ayelogin', methods=['GET', 'POST'])

def ayelogin():
    if current_user.is_authenticated:
        return redirect(url_for('ayeindex'))
    form=LoginForm()
    if form.validate_on_submit():
        user = VerifiedUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('ayelogin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('ayeindex')
        return redirect(next_page)
    return render_template('ayelogin.html', title='Sign In', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/ayehome', methods=['GET', 'POST'])

def ayeindex():
    return render_template('ayehome.html', title='Aye Home')

@app.route('/activitychecker', methods=['GET', 'POST'])
@login_required
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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.otp!=form.otp.data:
            flash('Wrong OTP. Please register again. {}')
            print(type(form.otp.data))
            User.query.filter_by(id=user.id).delete()
        else:
            u = VerifiedUser(email=user.email.data, username=user.username.data, firstname=user.firstname.data, lastname=user.lastname.data, phoneno=user.phoneno.data, employeecode=user.employeecode.data, password_hash=user.password.data)
            db.session.add(u)
            db.session.commit()
            return redirect('/index')
    return render_template('confirm.html', form=form)
