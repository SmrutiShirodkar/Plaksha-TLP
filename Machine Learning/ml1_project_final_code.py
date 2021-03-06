# -*- coding: utf-8 -*-
"""ml-project-keras-mlp-final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1777eVIuKW3mdCIxlOrSieWgR251xP-L_
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
 
np.random.seed(10)
state = np.random.RandomState(10)

from sklearn.model_selection import KFold
from sklearn import preprocessing
from sklearn import metrics
from sklearn.metrics import confusion_matrix

from google.colab import drive
drive.mount('/content/drive')
df_train = pd.read_csv('/content/drive/My Drive/Machine Learning/ML-1/Final Project/train.csv')
df_test = pd.read_csv('/content/drive/My Drive/Machine Learning/ML-1/Final Project/test.csv')

print(df_train.info())
print(df_train.shape)
print(df_train)
print(df_train.columns)

print(df_train[df_train.columns[1:19]].describe())

# df_train[df_train.columns[1:19]].hist(figsize=(20, 20), bins=100, xlabelsize=8, ylabelsize=8)

# df_new_train = df_train.drop(['lepton_2_pT','M_R','S_R','MT2',], axis=1)
# df_new_train.head(5)

X = df_train.drop(['Unnamed: 0','class'], axis = 1)
y = df_train['class']
print(y.unique())
print(df_train['class'].value_counts())
print(X.columns)

# from sklearn.preprocessing import MinMaxScaler

# # fit scaler on training data
# norm = MinMaxScaler().fit(X)

# # transform training data
# X = norm.transform(X)
# from sklearn.preprocessing import MinMaxScaler

# # fit scaler on training data
# norm = MinMaxScaler().fit(X)

# # transform training data
# X = norm.transform(X)

# X = X[:-325000]
# y = y[:-325000]

X = np.array(X)
print(type(X))
y = np.array(y)
print(type(y))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# from sklearn.model_selection import cross_val_score
# from keras.wrappers.scikit_learn import KerasClassifier


model = Sequential()
model.add(Dense(25,input_shape=(18,),activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(optimizer='adam',metrics=['accuracy'],loss='binary_crossentropy')

kf = KFold(n_splits=5,shuffle=True,random_state=10)
for k, (train_indices, test_indices) in enumerate(kf.split(X)):
  X_train, X_test = X[train_indices], X[test_indices]
  y_train, y_test = y[train_indices], y[test_indices]
  model.fit(X[train_indices], y[train_indices],epochs=15, batch_size=7550, verbose=1)
  loss, acc = model.evaluate(X_test, y_test, verbose=0)
  print("Accuracy: %.3f" % acc)

df_test.head()

df_test.info()
df_train.shape

df_test_new = df_test.drop(['Unnamed: 0'], axis = 1)

class_pred = model.predict(df_test_new)
class_output = pd.DataFrame()
class_output['Id'] = df_test.iloc[:, 0]
class_output['class'] = class_pred

class_output['class'].loc[class_output['class']> 0.5] = 1
class_output['class'].loc[class_output['class']<= 0.5] = 0

# To download the csv file locally
from google.colab import files
class_output.to_csv('prediction_colab_keras_5.csv',index=0)         
files.download('prediction_colab_keras_5.csv')