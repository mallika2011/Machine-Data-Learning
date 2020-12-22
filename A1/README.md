# Assignment 1 : Bias Variance Tradeoff

In this assigment we calculate the bias and variance of your trained model.

## Task 1
The dataset consists of pairs *(x<sub>i , y<sub>i)*. It is loaded into the python program using the pickle.load() function. The dataset is split into training and testing ```(90:10 split)```. We then divide the train set into 10 equal parts randomly, so that we get 10 different dataset to train our model.

After resampling, we now have 11 different datasets. We train a linear classifier on each of the 10 train set separately, so that we
have 10 different classifiers or models. Once we have 10 different models or classifiers trained separately on 10 different training set, we calculate the bias and variance of the model. 


## Task 2

Given a set of training data and a testing data we try to fit the given data to polynomials of degree 1 to 9(both inclusive) using the ```sklearn.linear_model.LinearRegression().fit()``` library. 

Given 20 subsets of training data containing 400 samples each, for each polynomial, we create 20 models trained on the 20 different
subsets and find the variance of the predictions on the testing data. Further we find the bias of the trained models on the testing data. Finally the bias-variance trade-Off graphs are plotted.