import numpy as np
import pickle 
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


with open('./data.pkl', 'rb') as f:
    data = pickle.load(f)

# print(data)   data stores all the data that is present
# train stores all the training data available
# test stores all the testing data available

size = data.shape[0]
np.random.shuffle(data)

x = int(0.9*size)   # x entries for training 90%
y = int(0.1*size)   # y entries for testing 10%

train=data[0:x,:]
test=data[x:size+1,:]
np.random.shuffle(test)

k=0
temp=[]
tempx=[]
tempy=[]

for i in range (10):
    temp.append(train[k:k+9,:])
    tempx.append(train[k:k+9,0])
    tempy.append(train[k:k+9,1])
    k+=9

f_train=np.array(temp)
x_train=np.array(tempx)
y_train=np.array(tempy)

print(x_train)
print(f_train[0])





