import numpy as np
import tester as server
import random

MAX_DEG=3 #number of features
key='847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'
range=10

def mutation(vector,index=-1):
    #chooses a random float in -range to +range and makes change at index position in vector

    #if no index is passed chooses a random index
    if index==-1:
        index=random.randint(0,MAX_DEG-1)

    vector[index]=random.uniform(-range,range)
    return vector

def crossover(vector1, vector2, index=-1):
    #performs a crossover from index onwards

    #if no index is passed chooses a random index
    send1=[]
    send2=[]

    if index==-1:
        index=random.randint(0,MAX_DEG-1)

        for i in range(MAX_DEG):
            parity=random.randint(0,1)
            if parity==1:
                send1.append(vector1[i])
                send2.append(vector2[i])
            else:
                send1.append(vector2[i])
                send2.append(vector1[i])
        return send1, send2

    else:
        for i in range(MAX_DEG):
            if i<index:
                send1.append(vector1[i])
                send2.append(vector2[i])
            else:
                send1.append(vector2[i])
                send2.append(vector1[i])
        return send1, send2

# how to choose individuals for crossover
# how to choose the next gen