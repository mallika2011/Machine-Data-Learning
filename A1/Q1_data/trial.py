import numpy as np
import pickle 
import matplotlib.pyplot as plot
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd


with open('./data.pkl', 'rb') as f:
    data = pickle.load(f)

# data stores all the data that is present
# train stores all the training data available
# test stores all the testing data available

size = data.shape[0]
np.random.shuffle(data)

x=data[:,:-1]
y=data[:,1]

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=1/10, random_state=0)

k=0
temp=[]
tempx=[]
tempy=[]

for i in range (10):
    tempx.append(x_train[k:k+450])
    tempy.append(y_train[k:k+450])
    k+=450

x_train=np.array(tempx)
y_train=np.array(tempy)

def func(x):
    x = x.ravel()

    return np.exp(-x ** 2) + 1.5 * np.exp(-(x - 2) ** 2)


v_table=np.zeros((10,10))
b_table=np.zeros((10,10))

bias_mean=np.zeros((9))
var_mean=np.zeros((9))

#For the polynomial degrees
for degree in range (1,10):  
    bias_sq=np.zeros((10,500))
    var=np.zeros((10,500))
    #For the training set
    for i in range (10):   
        poly = PolynomialFeatures(degree=degree, include_bias=False)

        #Transform the pilynomial features as required
        X = poly.fit_transform(x_train[i])
        X_TEST = poly.fit_transform(x_test)
        reg = LinearRegression()
        #Train the model for the chosen training set
        reg.fit(X, y_train[i])
        y_predict = reg.predict(X_TEST)

        # plot.scatter(x_train[i], y_train[i], color = 'red')
        # plot.scatter(x_train[i], reg.predict(X), color = 'blue')
        bias_sq[i]=((np.mean(y_predict) - y_test) ** 2)
        var[i]=(np.var(y_predict, axis=0))

    point_mean = np.mean(bias_sq,axis=0)
    bias_mean[degree-1]=np.mean(point_mean)
    point_var_mean = np.mean(var,axis=0)
    var_mean[degree-1]=np.mean(point_var_mean)

# print(pd.DataFrame(var_mean))
# print(pd.DataFrame(bias_mean))

print(var_mean)
print(bias_mean)


plot.plot(bias_mean,'b',label='Bias^2')
# plot.plot(var_mean,'r',label='Variance')
plot.xlabel('Complexity', fontsize='medium')
plot.ylabel('Error', fontsize='medium')
plot.title("Bias vs Variance")
plot.legend()
plot.show()



