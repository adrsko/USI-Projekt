import pandas as pd
import numpy as np
import joblib

def load(scaler_path, ohe_path, model_path):
        sc = joblib.load(scaler_path)
        ohe = joblib.load(ohe_path)
        model = joblib.load(model_path)
        return sc , ohe, model
row = [2010, 150000, 'Autmatyczna', 'benzyna']
cols = ['year', 'mileage','transmission', 'fuel_type']
sc, ohe, model = load('./jupyter/scaler.joblib', './jupyter/ohe.joblib', './jupyter/XGBoost.joblib')
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
print(prediction)