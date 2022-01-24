from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, SelectField, BooleanField
from flask_login import current_user
from flask import request
import json

class RegistrationForm(FlaskForm):
    username = StringField('Login: ')
    email = StringField('Email: ')
    password = PasswordField('Hasło: ' , validators=[DataRequired(), validators.Length(min=5, max=50, message='Hasło musi mieć przynajmniej 5 znaków'), validators.EqualTo('confirm_password', message='Hasła muszą być takie same')])
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
    from main import Cars, db
    query2 = db.session.query(Cars.model.distinct().label("model")).order_by(Cars.model)
    models = [row.model for row in query2.all()]
    model = SelectField(u'Marka:', choices=models)
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    price = IntegerField('Cena: ')
    fuel_type = SelectField(u'Typ Paliwa:', choices=[('Benzyna', 'Benzyna'),('Diesel', 'Diesel')])
    transmission = SelectField(u'Skrzynia Biegów:', choices=[('Manualna', 'Manualna'),('Automatyczna', 'Automatyczna')])
    submit = SubmitField('Zapisz')

class UpdateCarForm(FlaskForm):
    from main import Cars, db
    query2 = db.session.query(Cars.model.distinct().label("model")).order_by(Cars.model)
    models = [row.model for row in query2.all()]
    model = SelectField(u'Marka:', choices=models)
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    fuel_type = SelectField(u'Typ Paliwa:', choices=[('Benzyna', 'Benzyna'),('Diesel', 'Diesel')])
    transmission = SelectField(u'Skrzynia Biegów:', choices=[('Manualna', 'Manualna'),('Automatyczna', 'Automatyczna')])
    price = IntegerField('Cena: ')
    submit = SubmitField('Zapisz')


class PricesForm(FlaskForm):
    from main import Cars, db
    from sqlalchemy import desc
    query2 = db.session.query(Cars.model.distinct().label("model")).order_by(Cars.model)
    models = [row.model for row in query2.all()]
    model = SelectField(u'Marka:', choices=models)
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    fuel_type = SelectField(u'Typ Paliwa:', choices=[('Benzyna', 'Benzyna'),('Diesel', 'Diesel')])
    transmission = SelectField(u'Skrzynia Biegów:', choices=[('Manualna', 'Manualna'),('Automatyczna', 'Automatyczna')])
    submit = SubmitField('Oblicz przewidywany koszt samochodu')

