import numpy as np
import pickle 
import matplotlib.pyplot as plot

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


with open('./data.pkl', 'rb') as f:
    data = pickle.load(f)

# print(data)   data stores all the data that is present
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
    tempx.append(x_train[k:k+9])
    tempy.append(y_train[k:k+9])
    k+=9

x_train=np.array(tempx)
y_train=np.array(tempy)

print(x_train)

for degree in range (1,9):  #For the polynomial degrees
    for i in range (10):    #For the training set
        reg = LinearRegression()
        reg.fit(x_train[i], y_train[i])
        plot.scatter(x_train[i], y_train[i], color = 'red')
        plot.plot(x_train[i], reg.predict(x_train[i]), color = 'blue')
        plot.title('X vs Y (Training set)')
        plot.xlabel('X-axis')
        plot.ylabel('Y-axis')
        plot.show()





