import numpy as np
import pickle 
import matplotlib.pyplot as plot
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd


with open('./Fx_test.pkl', 'rb') as f:
    Fox_test = pickle.load(f)  #Testing set for f(x)
with open('./X_test.pkl', 'rb') as f:
    x_test = pickle.load(f)    #Testing set for x
with open('./X_train.pkl', 'rb') as f:
    x_train = pickle.load(f)   #Training set for x
with open('./Y_train.pkl', 'rb') as f:
    y_train = pickle.load(f)   #Training set for y 

x_test=x_test.reshape(-1,1)

v_table=np.zeros((10,10))
b_table=np.zeros((10,10))

bias_mean=np.zeros((9))
var_mean=np.zeros((9))

#For the polynomial degrees
for degree in range (1,10):  
    bias_sq=np.zeros((20,80))
    var=np.zeros((20,80))
    out=np.zeros((20,80))
    #For the training set
    for i in range (20):   
        poly = PolynomialFeatures(degree=degree, include_bias=False)

        #Transform the polynomial features as required
        X = poly.fit_transform(x_train[i].reshape(-1,1))
        X_TEST = poly.fit_transform(x_test)
        reg = LinearRegression()

        #Train the model for the chosen training set
        reg.fit(X, y_train[i])
        y_predict = reg.predict(X_TEST)
        if(i==1):
            plot.scatter(x_train[i], y_train[i], color = 'red')
            plot.scatter(x_train[i], reg.predict(X), color = 'blue')
            plot.show()
        out[i]=y_predict

    #calculate bias
    point_mean = np.mean(out,axis=0)
    bias_mean[degree-1]=np.mean((point_mean-Fox_test)**2)

    #calculate variance
    point_var = np.var(out,axis=0)
    var_mean[degree-1]=np.mean(point_var)


table_bias=pd.DataFrame({'Degree':np.array(range(1,10)),'Bias^2':bias_mean,'Variance': var_mean})
print(table_bias.to_string(index=False))

plot.plot(bias_mean,'b',label='Bias^2')
plot.plot(var_mean,'r',label='Variance')
plot.xlabel('Complexity', fontsize='medium')
plot.ylabel('Error', fontsize='medium')
plot.title("Bias vs Variance")
plot.legend()
plot.show()