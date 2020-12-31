import numpy as np

MAX_DEG=11 #number of features
weights=np.array((1,2,3,4,5,1,-1,1,-7,1,1),float)

hi=5
lo=-5

x_train=(hi-lo)*np.random.random_sample((1000,MAX_DEG))+lo
y_train=np.sum(weights*x_train,axis=1)

x_test=(hi-lo)*np.random.random_sample((1000,MAX_DEG))+lo
y_test=np.sum(weights*x_test,axis=1)

def get_errors(id,vector):

    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG
    ans=[]
    y_out_train=np.sum(vector*x_train,axis=1)

    mse1=np.mean((y_out_train-y_train)*(y_out_train-y_train))
    ans.append(mse1)

    y_out_test=np.sum(vector*x_test,axis=1)
    mse2=np.mean((y_out_test-y_test)*(y_out_test-y_test))
    ans.append(mse2)

    return ans


def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG
    return 'successfully submitted'

# print(get_errors('as',[1,1,3]))
