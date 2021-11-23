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
    model=pickle.load(open("LinearRegressionModel.pkl", 'rb'))
    prediction = model.predict(pd.DataFrame([['BMW', 'X4', 2021, 40000, 'benzyna', 'manualna']], columns=['brand', 'model', 'year', 'mileage', 'fuel_type', 'transmission']))
    print(prediction)

test()