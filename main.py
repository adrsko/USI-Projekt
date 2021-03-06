from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user
import uuid
from sqlalchemy_utils import ChoiceType
from sqlalchemy import exists

app = Flask(__name__)

app.config['SECRET_KEY']='3df59cf36c028e0c0beef6c696504755'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Cars(db.Model):

    CHOICES = [('Benzyna', 'Benzyna'),('Diesel', 'Diesel')]
    CHOICES2 = [('Manualna', 'Manualna'),('Automatyczna', 'Automatyczna')]

    id = db.Column(db.String(100), primary_key=True, nullable=False)
    model = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(ChoiceType(CHOICES))
    transmission = db.Column(ChoiceType(CHOICES2))
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Cars('{self.model}')"

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route("/cars/<int:page_num>",methods=['GET'])
def cars(page_num):
    if current_user.is_authenticated:
        cars = Cars.query.paginate(per_page=12, page=page_num, error_out=False)
        return render_template('cars.html', cars=cars)
    else:
        return redirect(url_for('login'))

@app.route("/prices", methods=['GET', 'POST'])
def prices():
    if current_user.is_authenticated:
        from form import PricesForm
        form = PricesForm()
        return render_template('prices.html', title='Add_car', form = form)
    else:
        return redirect(url_for('login'))

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    from form import PricesForm
    import pandas as pd
    import numpy as np
    import joblib
    form = PricesForm()
    model = form.model.data
    year = form.year.data
    mileage = form.mileage.data
    fuel_type = form.fuel_type.data
    transmission = form.transmission.data
    def load(scaler_path, ohe_path, model_path):
        sc = joblib.load(scaler_path)
        ohe = joblib.load(ohe_path)
        model = joblib.load(model_path)
        return sc , ohe, model
    row = [model, year, mileage, transmission, fuel_type]
    cols = ['model', 'year', 'mileage','transmission', 'fuel_type']
    sc, ohe, model = load('scaler.joblib', 'ohe.joblib', 'XGBoost.joblib')
    df = pd.DataFrame([row], columns = cols)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    car_num_cols = list(df.select_dtypes(include=numerics).columns)
    df[car_num_cols] = sc.transform(df[car_num_cols])
    car_cat_cols = list(df.select_dtypes(exclude=numerics).columns)
    car_ohe = ohe.transform(df[car_cat_cols])
    car_df_ohe = pd.DataFrame(car_ohe, columns = ohe.get_feature_names_out(input_features = car_cat_cols))
    df = df.drop(car_cat_cols, axis=1)
    df = pd.concat([df, car_df_ohe], axis=1)
    prediction = model.predict(df)[0]
    return str(prediction)
    
@app.route("/register", methods = ['GET', 'POST'])
def register():
    from form import RegistrationForm
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(id = str(uuid.uuid4()), username=form.username.data, email=form.email.data, password=hashed_password)
            if db.session.query(exists().where(User.username==form.username.data)).scalar():
                flash("Podany login ju?? istnieje, wybierz inny")
            elif db.session.query(exists().where(User.email==form.email.data)).scalar():
                flash("Podany email ju?? istnieje, wybierz inny")
            else:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    from form import LoginForm
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
    from form import UpdateAccountForm
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

@app.route("/add_car", methods = ['GET', 'POST'])
def add_car():
    from form import AddCarForm
    if current_user.is_authenticated:
        form = AddCarForm()
        if form.validate_on_submit():
            car = Cars(id = str(uuid.uuid4()), model=form.model.data, year=form.year.data, mileage=form.mileage.data, fuel_type=form.fuel_type.data, transmission=form.transmission.data, price=form.price.data)
            db.session.add(car)
            db.session.commit()
            return redirect(url_for('cars', page_num=1))
        return render_template('add_car.html', title='Add_car', form=form)
    else:
        return redirect(url_for('login'))

@app.route("/cars/<id>", methods = ['GET', 'POST'])
def edit_car(id):
    from form import UpdateCarForm
    if current_user.is_authenticated:
        edit_car = Cars.query.filter_by(id=id).first()
        form = UpdateCarForm()
        if form.validate_on_submit():
            edit_car.model = form.model.data
            edit_car.year = form.year.data
            edit_car.mileage = form.mileage.data
            edit_car.fuel_type = form.fuel_type.data
            edit_car.transmission = form.transmission.data
            edit_car.price = form.price.data
            db.session.commit()
            return redirect(url_for('cars', page_num=1))
        elif request.method == 'GET':
            form.model.data = edit_car.model
            form.year.data = edit_car.year
            form.mileage.data = edit_car.mileage
            form.fuel_type.data = edit_car.fuel_type
            form.transmission.data = edit_car.transmission
            form.price.data = edit_car.price
        return render_template('edit_car.html', title='Add_car', form=form)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)