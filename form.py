from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Email, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, SelectField, BooleanField
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
    fuel_type = SelectField(u'Typ Paliwa:', choices=[('benzyna', 'Benzyna'),('diesel', 'Diesel')])
    transmission = SelectField(u'Skrzynia Biegów:', choices=[('manulana', 'Manualna'),('automatyczna', 'Automatyczna')])
    submit = SubmitField('Zapisz')

class UpdateCarForm(FlaskForm):
    brand = StringField('Marka: ')
    model = StringField('Model: ')
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    fuel_type = SelectField(u'Typ Paliwa:', choices=[('benzyna', 'Benzyna'),('diesel', 'Diesel')])
    transmission = SelectField(u'Skrzynia Biegów:', choices=[('manulana', 'Manualna'),('automatyczna', 'Automatyczna')])
    price = IntegerField('Cena: ')
    submit = SubmitField('Zapisz')



class PricesForm(FlaskForm):
    from main import Cars, db
    query = db.session.query(Cars.brand.distinct().label("brand"))
    brands = [row.brand for row in query.all()]
    query2 = db.session.query(Cars.model.distinct().label("model"))
    models = [row.model for row in query2.all()]
    brand = SelectField(u'Marka:', choices=brands)
    model = SelectField(u'Marka:', choices=models)
    year = IntegerField('Rok: ')
    mileage = IntegerField('Przebieg: ')
    fuel_type = SelectField(u'Typ Paliwa:', choices=[('benzyna', 'benzyna'),('diesel', 'diesel')])
    transmission = SelectField(u'Skrzynia Biegów:', choices=[('manualna', 'manualna'),('automatyczna', 'automatyczna')])
    submit = SubmitField('Oblicz przewidywany koszt samochodu')

class RegressionForm(FlaskForm):
    submit = SubmitField('Oblicz Regresję')


