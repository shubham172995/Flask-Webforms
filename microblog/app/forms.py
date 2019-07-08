from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phoneno = StringField('Phone Number', validators=[DataRequired()])
    employeecode = StringField('Employee Code', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('EMAIL', validators=[DataRequired()])
    submit = SubmitField('Register')

class ActivityForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Aye Employee Password', validators=[DataRequired()])
    activity = StringField('Activate/Deactivate', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ConfirmationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    otp = StringField('OTP', validators=[DataRequired()])
    submit = SubmitField('Submit')
