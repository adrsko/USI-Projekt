import pandas as pd 
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
import pickle


def test():
    lst=[]
    engine = create_engine('sqlite:///site.db')
    for i in range(len(engine.connect().execute("select model from Cars where brand = " + "'BMW'").unique().all())):
        test = engine.connect().execute("select model from Cars where brand = " + "'BMW'").unique().all()[i]
        for row in test:
            lst.append(row)
    print(lst)


test()