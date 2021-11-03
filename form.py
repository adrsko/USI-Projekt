from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Email, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Login: ')
    email = StringField('Email: ')
    password = PasswordField('Hasło: ')
    confirm_password = PasswordField('Powtórz Hasło: ')
    submit = SubmitField('Zarejestruj się')

class LoginForm(FlaskForm):
    email = StringField('Email:')
    password = PasswordField('Hasło')
    submit = SubmitField('Zaloguj się')
