from enum import unique
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from form import LoginForm, RegistrationForm, UpdateAccountForm
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY']='3df59cf36c028e0c0beef6c696504755'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    brand = db.Column(db.String(60), unique=True, nullable=False)
    model = db.Column(db.String(60), unique=True, nullable=False)
    year = db.Column(db.Integer, primary_key=True, nullable=False)
    mileage = db.Column(db.Integer, primary_key=True, nullable=False)
    price = db.Column(db.Integer, primary_key=True, nullable=False)

    def __repr__(self):
        return f"Cars('{self.brand}', '{self.model}')"


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route("/cars")
def cars():
    if current_user.is_authenticated:
        cars = Cars.query.all()
        return render_template('cars.html', cars=cars)
    else:
        return redirect(url_for('login'))

@app.route("/prices")
def prices():
    if current_user.is_authenticated:
        return render_template('prices.html')
    else:
        return redirect(url_for('login'))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html', title='Login', form=form)
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return render_template('home.html')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods = ['GET', 'POST'])
def account():
    if current_user.is_authenticated:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        return render_template('account.html', title='Account', form=form)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)