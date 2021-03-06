#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import read_csv
train = read_csv('data_inr.csv', header=None, index_col=0, parse_dates=True, squeeze=True)
train
from numpy import sqrt
import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

import datetime
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import Holt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA


# In[2]:


df1=pd.read_csv("C:/Users/Admin/Documents/P-99/data_inr.csv",header=0, names=["Date","Rate"])


# In[3]:


df1


# In[4]:


Train = df1.head(326)
Test = df1[326:]


# In[5]:


Train


# In[6]:


Test


# In[7]:


def MAPE(pred,org):
    temp = np.abs((pred-org)/org)*100
    return np.mean(temp)


# In[8]:


df1['Date'] = pd.to_datetime(df1['Date'],errors='coerce')


# In[9]:


df1["month"] = df1.Date.dt.strftime("%b")
df1["year"] = df1.Date.dt.strftime("%Y")


# In[10]:


df1


# In[11]:


import statsmodels.graphics.tsaplots as tsa_plots
tsa_plots.plot_acf(df1.Rate,lags=12)
tsa_plots.plot_pacf(df1.Rate,lags=12)
plt.show()


# # SIMPLE EXPONENTIAL METHOD

# In[12]:


ses_model = SimpleExpSmoothing(Train['Rate']).fit(smoothing_level=0.2)
pred_ses = ses_model.predict(start = Test.index[0],end = Test.index[-1])
MAPE(pred_ses,Test.Rate) 


# # HOLT METHOD

# In[13]:


# Holt method 
hw_model = Holt(Train["Rate"]).fit(smoothing_level=0.8, smoothing_slope=0.2)
pred_hw = hw_model.predict(start = Test.index[0],end = Test.index[-1])
MAPE(pred_hw,Test.Rate)


# # Holts winter exponential smoothing with additive seasonality and additive trend

# In[14]:


from statsmodels.tsa.holtwinters import ExponentialSmoothing 


# In[15]:


hwe_model_add_add = ExponentialSmoothing(Train["Rate"],seasonal="add",trend="add",seasonal_periods=12).fit() #add the trend to the model
pred_hwe_add_add = hwe_model_add_add.predict(start = Test.index[0],end = Test.index[-1])
MAPE(pred_hwe_add_add,Test.Rate) 


# # Holts winter exponential smoothing with multiplicative seasonality and additive trend

# In[16]:


#Forecasting for next 10 time periods
hw_model.forecast(30)


# # ARIMA Hyperparameters

# In[17]:


# grid search ARIMA parameters for a time series

import warnings
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt


# evaluate an ARIMA model for a given order (p,d,q) and return RMSE
def evaluate_arima_model(X, arima_order):
# prepare training dataset
    X = X.astype('float32')
    train_size = int(len(X) * 0.50)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
# make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
# model_fit = model.fit(disp=0)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
# calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))
    return rmse


# # Grid search for p,d,q values

# In[18]:


# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float('inf'), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    rmse = evaluate_arima_model(train, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    print('ARIMA%s RMSE=%.3f' % (order,rmse))
                except:
                    continue
    print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))


# # Combine train and test data and build final model

# In[ ]:





# In[19]:


# fit model
df = read_csv("C:/Users/Admin/Documents/P-99/data_inr.csv", header=0, index_col=0, parse_dates=True)
# prepare data
X = train.values
X = X.astype('float32')


# In[20]:


model = ARIMA(X, order=(3,1,0))
model_fit = model.fit()


# In[21]:


forecast=model_fit.forecast(steps=10)[0]
model_fit.plot_predict(1,80)


# In[ ]:





# In[ ]:




