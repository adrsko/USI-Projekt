from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Email, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField
from flask_login import current_user

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

class UpdateAccountForm(FlaskForm):
    username = StringField('Login: ')
    email = StringField('Email: ')
    submit = SubmitField('Zapisz')

class AddCarForm(FlaskForm):
    brand = StringField('Marka: ')
    model = StringField('Model: ')
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    price = IntegerField('Cena: ')
    submit = SubmitField('Zapisz')

class UpdateCarForm(FlaskForm):
    brand = StringField('Marka: ')
    model = StringField('Model: ')
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    price = IntegerField('Cena: ')
    submit = SubmitField('Zapisz')
