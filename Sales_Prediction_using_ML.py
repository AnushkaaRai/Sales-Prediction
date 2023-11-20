# -*- coding: utf-8 -*-
"""Sales Prediction using Machine Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VpI_kg3SidWSSq9TsVRtt3D6Ad-6M7hR
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

data = pd.read_csv('/content/drive/MyDrive/home/sales_prediction.csv')

data.sample(5)

"""### Find Shape of Our Dataset (Number of Rows And Number of Columns)"""

data.shape

"""### Get Information About Our Dataset Like Total Number Rows, Total Number of Columns, Datatypes of Each Column And Memory Requirement"""

data.describe()

"""### Check Null Values In The Dataset"""

data.isnull().sum()

per = data.isnull().sum() * 100 / len(data)
print(per)

"""### Taking Care of Duplicate Values"""

data.duplicated().any()



"""### Handling The missing Values"""

data['Item_Weight']

data['Outlet_Size']

"""### Univariate Imputation"""

mean_weight = data['Item_Weight'].mean()
median_weight = data['Item_Weight'].median()

print(mean_weight,median_weight)

data['Item_Weight_mean']=data['Item_Weight'].fillna(mean_weight)
data['Item_Weight_median']=data['Item_Weight'].fillna(median_weight)

data.head(1)

print("Original Weight variable variance",data['Item_Weight'].var())
print("Item Weight variance after mean imputation",data['Item_Weight_mean'].var())
print("Item Weight variance after median imputation",data['Item_Weight_median'].var())

data['Item_Weight'].plot(kind = "kde",label="Original")

data['Item_Weight_mean'].plot(kind = "kde",label = "Mean")

data['Item_Weight_median'].plot(kind = "kde",label = "Median")

plt.legend()
plt.show()

data[['Item_Weight','Item_Weight_mean','Item_Weight_median']].boxplot()

data['Item_Weight_interploate']=data['Item_Weight'].interpolate(method="linear")

data['Item_Weight'].plot(kind = "kde",label="Original")

data['Item_Weight_interploate'].plot(kind = "kde",label = "interploate")

plt.legend()
plt.show()



"""### Multivariate Imputaion"""

from sklearn.impute import KNNImputer

knn = KNNImputer(n_neighbors=10,weights="distance")

data['knn_imputer']= knn.fit_transform(data[['Item_Weight']]).ravel()

data['Item_Weight'].plot(kind = "kde",label="Original")

data['knn_imputer'].plot(kind = "kde",label = "KNN imputer")

plt.legend()
plt.show()

data = data.drop(['Item_Weight','Item_Weight_mean','Item_Weight_median','knn_imputer'],axis=1)

data.head(1)

data.isnull().sum()

"""### Outlet_Size"""

data['Outlet_Size'].value_counts()

data['Outlet_Type'].value_counts()

mode_outlet = data.pivot_table(values='Outlet_Size',columns='Outlet_Type',aggfunc=(lambda x:x.mode()[0]))

mode_outlet

missing_values = data['Outlet_Size'].isnull()

missing_values

data.loc[missing_values,'Outlet_Size'] = data.loc[missing_values,'Outlet_Type'].apply(lambda x :mode_outlet[x])

data.isnull().sum()

"""### Item_Fat_Content"""

data.columns

data['Item_Fat_Content'].value_counts()

data.replace({'Item_Fat_Content':{'Low Fat':'LF','low fat':'LF','reg':'Regular'}},inplace=True)

data['Item_Fat_Content'].value_counts()

"""### Item_Visibility"""

data.columns

data['Item_Visibility'].value_counts()

data['Item_Visibility_interpolate']=data['Item_Visibility'].replace(0,np.nan).interpolate(method='linear')

data.head(1)

data['Item_Visibility_interpolate'].value_counts()

data['Item_Visibility'].plot(kind="kde",label="Original")

data['Item_Visibility_interpolate'].plot(kind="kde",color='red',label="Interpolate")

plt.legend()
plt.show()

data = data.drop('Item_Visibility',axis=1)

data.head(1)

"""### Item_Type"""

data.columns

data['Item_Type'].value_counts()

"""### Item_Identifier"""

data.columns

data['Item_Identifier'].value_counts().sample(5)

data['Item_Identifier'] =data['Item_Identifier'].apply(lambda x : x[:2])

data['Item_Identifier'].value_counts()

"""### Outlet_Establishment_Year"""

data.columns

data['Outlet_Establishment_Year']

import datetime as dt

current_year = dt.datetime.today().year

current_year

data['Outlet_age']= current_year - data['Outlet_Establishment_Year']

data.head(1)

data = data.drop('Outlet_Establishment_Year',axis=1)

data.head()

"""### Handling Categorical Columns"""

from sklearn.preprocessing import OrdinalEncoder

data_encoded = data.copy()

cat_cols = data.select_dtypes(include=['object']).columns

for col in cat_cols:
    oe = OrdinalEncoder()
    data_encoded[col]=oe.fit_transform(data_encoded[[col]])
    print(oe.categories_)

data_encoded.head(3)

X = data_encoded.drop('Item_Outlet_Sales',axis=1)
y = data_encoded['Item_Outlet_Sales']

y

"""### Random Forest Regressor"""

from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import cross_val_score

rf = RandomForestRegressor(n_estimators=100,random_state=42)
scores = cross_val_score(rf,X,y,cv=5,scoring='r2')
print(scores.mean())



"""### XGBRFRegressor"""

from xgboost import XGBRFRegressor

xg = XGBRFRegressor(n_estimators=100,random_state=42)
scores = cross_val_score(xg,X,y,cv=5,scoring='r2')
print(scores.mean())

X = data_encoded.drop('Item_Outlet_Sales', axis=1).values
y = data_encoded['Item_Outlet_Sales'].values

"""grad

"""

from sklearn.ensemble import GradientBoostingRegressor

# Rest of your code...
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_scores = cross_val_score(gb, X, y, cv=5, scoring='r2')
print(f'Gradient Boosting Regressor R2 Score: {np.mean(gb_scores)}')

"""hist

"""

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import HistGradientBoostingRegressor
import numpy as np

# Assuming X and y are defined and have the correct dimensions

hist = HistGradientBoostingRegressor(random_state=42)
hist_scores = cross_val_score(hist, X, y, cv=5, scoring='r2')
print(f'Hist Gradient Boosting Regressor R2 Score: {np.mean(hist_scores)}')

X = data_encoded.drop('Item_Outlet_Sales',axis=1)
y = data_encoded['Item_Outlet_Sales']

"""### XGBRFRegressor Feature importances"""

xg = XGBRFRegressor(n_estimators=100, random_state=42)
xg1 = xg.fit(X, y)

# If X is a pandas DataFrame
feature_importances = pd.DataFrame({
    'feature': X.columns,
    'XGBRF_importance': xg1.feature_importances_
}).sort_values(by='XGBRF_importance', ascending=False)

# Assuming X is a pandas DataFrame
feature_importances = pd.DataFrame({
    'feature': X.columns,
    'XGBRF_importance': xg1.feature_importances_
}).sort_values(by='XGBRF_importance', ascending=False)

# If X is a NumPy array
num_features = X.shape[1]
dummy_columns = [f'Feature_{i}' for i in range(num_features)]

feature_importances = pd.DataFrame({
    'feature': dummy_columns,
    'XGBRF_importance': xg1.feature_importances_
}).sort_values(by='XGBRF_importance', ascending=False)

['Item_Visibility_interpolate','Item_Weight_interploate',
'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content']

from xgboost import XGBRFRegressor

xg = XGBRFRegressor(n_estimators=100,random_state=42)
scores = cross_val_score(xg1,X.drop(['Item_Visibility_interpolate','Item_Weight_interploate',
'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content'],axis=1),y,cv=5,scoring='r2')
print(scores.mean())

final_data = X.drop(columns=['Item_Visibility_interpolate','Item_Weight_interploate',
'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content'],axis=1)

final_data



"""### Best Model"""

from xgboost import XGBRFRegressor

xg_final = XGBRFRegressor()

xg_final.fit(final_data,y)

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X_train,X_test,y_train,y_test = train_test_split(final_data,y,
                                                 test_size=0.20,
                                                 random_state=42)

xg_final.fit(X_train,y_train)

y_pred = xg_final.predict(X_test)

mean_absolute_error(y_test,y_pred)

"""### Prediction on Unseen Data"""

pred = xg_final.predict(np.array([[141.6180,9.0,1.0,1.0,24]]))[0]
print(pred)

print(f"Sales Value is between {pred-714.42} and {pred+714.42}")