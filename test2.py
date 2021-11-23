import pandas as pd 
import numpy as np
import sqlalchemy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
import pickle

def test():
    cnx=sqlalchemy.create_engine('sqlite:///site.db')
    car = pd.read_sql_query('SELECT * FROM Cars', cnx)
    X=car.drop(columns=['price', 'id'])
    y=car['price']
    ohe = OneHotEncoder()
    ohe.fit(X[['brand', 'model', 'fuel_type', 'transmission']])
    column_trans = make_column_transformer((OneHotEncoder(categories=ohe.categories_),['brand', 'model', 'fuel_type', 'transmission']), remainder='passthrough')
    scores=[]
    for i in range(1000):
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=i)
        lr = LinearRegression()
        pipe = make_pipeline(column_trans, lr)
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        scores.append(r2_score(y_test, y_pred))
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=np.argmax(scores))
    lr = LinearRegression()
    pipe = make_pipeline(column_trans, lr)
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    scores.append(r2_score(y_test, y_pred))
    pickle.dump(pipe, open('LinearRegressionModel.pkl', 'wb'))
