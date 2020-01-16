from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

## Creates a class for the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField('Login')

## Creates a class for the signup form
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired(), EqualTo('test_password', message="Passwords must match")])
    test_password = PasswordField('Repeat Password')
    submit = SubmitField('Register')
