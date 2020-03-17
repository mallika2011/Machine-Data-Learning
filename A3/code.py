import numpy as np
import tester as server
import random

MAX_DEG=3 #number of features
key='847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'
ranger=10
pc=0.2 

def mutation(vector,index=-1):
    #chooses a random float in -range to +range and makes change at index position in vector

    #if no index is passed chooses a random index
    if index==-1:
        index=random.randint(0,MAX_DEG-1)

    #here probability is 0.5
    parity=random.randint(0,1)
    if parity==1:
        vector[index]=random.uniform(-ranger,ranger)
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

def choose(options,size=1):
    send=[]

    for vec in options()
        server.get_errors(id,)


# how to choose individuals for crossover
# how to choose the next gen


#main

#generate initial genration (mutation) size 100

#while loop
    #create a utility array that stores the error for every individual in the population
    #parenterrors[]
    #get the probability of selection for every parent for going into crossover, this will generate the probaliliites based on the error
    #above function will return an array: parentprobality

    #for i in range(number of time you want to do crossover):
    #   pick two parents using numpy.random.choice
    #   cross them over, now we have two new
    #   choose between them. how? -> top two? according to probability?
    #   for now, choose only the children ignore the parents
    #   mutate the crossovers
    #   put them into an array called nextgen[]
