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

var_final=[]
bias_final=[]

#For the polynomial degrees
for degree in range (1,10):  
    arr=[]
    #For the training set
    for i in range (20):   
        poly = PolynomialFeatures(degree=degree, include_bias=False)

        #Transform the pilynomial features as required
        X = poly.fit_transform(x_train[i].reshape(-1,1))
        X_TEST = poly.fit_transform(x_test)
        reg = LinearRegression()
        #Train the model for the chosen training set
        reg.fit(X, y_train[i])
        y_predict = reg.predict(X_TEST)
        print(y_predict)
        # plot.scatter(x_train[i], y_train[i], color = 'red')
        # plot.scatter(x_train[i], reg.predict(X), color = 'blue')
        arr.append(y_predict)
    
    arr=np.array(arr)
    bias_mean=np.mean(arr,axis=0)
    bias_sq=((bias_mean - Fox_test) ** 2)
    var=np.var(arr,axis=0)
    bias_final.append(np.average(bias_sq))
    var_final.append(np.average(var))

bias_final=np.array(bias_final)
var_final=np.array(var_final)

print(pd.DataFrame(var_final))
print(pd.DataFrame(bias_final))

# print(var_final)
# print(bias_mean)


plot.plot(bias_final,'b',label='Bias')
plot.plot(var_final,'r',label='Variance')
plot.xlabel('Complexity', fontsize='medium')
plot.ylabel('Error', fontsize='medium')
plot.title("Bias vs Variance")
plot.legend()
plot.show()



