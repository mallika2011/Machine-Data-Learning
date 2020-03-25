import numpy as np
# import tester as server
import client_moodle as server
import random

team_name="team_62" #for our reference
MAX_DEG=11 #number of features
key='847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'
ranger=10
pc=0.2 
pop_size=100
cross_n=int(pop_size/2)
iter=40

def mutation(vector,index=-1,mut_prob=0.1):
    #chooses a random float in -range to +range and makes change at index position in vector

    #if no index is passed chooses a random index
    if index==-1:
        index=random.randint(0,MAX_DEG-1)

    #here probability is 0.5
    parity=random.randint(0,1)
    # print("Parity",parity)
    if parity==1:
        vector[index]=random.uniform(-ranger,ranger)
    return vector

def mutateall(vector):

    for i in range(len(vector)):
        vector=mutation(vector,i,0.85)
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

#flow of the program
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

def gen_parent_probabilities(size):
    parentprobalities=np.zeros(size)
    for j in range(size-1):
        parentprobalities[j]=((1-pc)**j)*pc
    #assign last probability
    parentprobalities[size-1]=((1-pc)**(size-1))
    return parentprobalities

def crossover_select(parentprobalities):
    parents=[]
    # i1=np.random.choice(np.arange(0,pop_size),p=parentprobalities)
    # i2=np.random.choice(np.arange(0,pop_size),2 replace=False,p=parentprobalities)
    # parents.append(i1)
    # parents.append(i2)
    parents=np.random.choice(np.arange(0,pop_size),2, replace=False,p=parentprobalities)
    return parents

def main():
    print("PC: " ,pc, " POP_SIZE: ",pop_size," ITER : ", iter)

    vector_og=[0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
    # vector_og=[-9.78736351e+00 ,-6.30079234e+00 ,-5.86904268e+00 , 4.93390314e-02,3.81084816e-02 , 8.13236610e-05, -6.01876916e-05, -1.25158557e-07,3.48409638e-08,  4.16149250e-11, -6.73242018e-12]
    to_send=[-20,-20,-20,-20,-20,-20,-20,-20,-20,-20,-20]
    min_error=-1
    min_error1=-1
    min_error2=-1

    parenterrors=np.zeros(pop_size)
    parenterrors1=np.zeros(pop_size)
    parenterrors2=np.zeros(pop_size)
    parentprobalities=np.zeros(pop_size)
    population=np.zeros((pop_size,MAX_DEG))

    # generate the population 
    for i in range(pop_size):
        temp=np.copy(vector_og)
        population[i]=mutateall(temp)

    #generate errors for each individual in the population
    for j in range(pop_size):
        temp=population[j].tolist() #passing a list to the get_errors function
        err=server.get_errors(key,temp)
        
        #adding the two errors and storing in parenterror
        parenterrors[j]=(err[0]+err[1])
        parenterrors1[j]=(err[0])
        parenterrors2[j]=(err[1])

    # have to change this to a while loop with appropriate condition later
    for iter_num in range(iter):
        new_iter=0

        print("\n\n\n\n********"+str(iter_num)+"*********")


        # Sort the errors in ascending order
        # Least error => max fittness
        # Correspondingly sort the population also
        parenterrorsinds=parenterrors.argsort()
        parenterrors=parenterrors[parenterrorsinds[::1]]
        parenterrors1=parenterrors1[parenterrorsinds[::1]]
        parenterrors2=parenterrors2[parenterrorsinds[::1]]
        population=population[parenterrorsinds[::1]]


        #debug statements
        for j in range(pop_size):
            print("person " + str(j)+" error "+ str(parenterrors[j]))
            print("\tvalues"+str(population[j])+"\n\n")

        # Assign probabilities to the population
        parentprobalities=gen_parent_probabilities(pop_size)
        
        # Checking sum(prob) = 1
        # print(np.sum(parentprobalities))
        child_population=np.zeros((pop_size,MAX_DEG))

        #perform crossover cross_n times
        for j in range (cross_n):
            arr=crossover_select(parentprobalities)
            
            # Two parents chosen based on probabilities => arr[0], arr[1]
            # Sending parents for crossover
            temp=crossover(population[arr[0]],population[arr[1]])
            
            child_population[new_iter]=temp[0]
            new_iter+=1

            child_population[new_iter]=temp[1]    
            new_iter+=1

        # print("BEFORE MUTATION: CHILD POPULATION")
        # for j in range(len(child_population)):
        #     print("Child", j)
        #     print(child_population[i])

        # Send the new population for mutation
        for j in range(pop_size):
            temp=np.copy(child_population[j])
            child_population[j]=mutation(temp)

        # print("AFTER MUTATION: CHILD POPULATION")
        # for j in range(len(child_population)):
        #     print("Child", j)
        #     print(child_population[i])

        # get the errors for the new population
        childerrors=np.zeros(pop_size)
        childerrors1=np.zeros(pop_size)
        childerrors2=np.zeros(pop_size)

        # generate errors for each child
        for j in range(pop_size):
            temp=child_population[j].tolist() #passing a list to the get_errors function
            err=server.get_errors(key,temp)
            
            #adding the two errors and storing in parenterror
            childerrors[j]=(err[0]+err[1])
            childerrors1[j]=(err[0])
            childerrors2[j]=(err[1])

        #combining parents and children into one array
        candidates=np.concatenate([population,child_population])
        candidate_errors=np.concatenate([parenterrors,childerrors])
        candidate_errors1=np.concatenate([parenterrors1,childerrors1])
        candidate_errors2=np.concatenate([parenterrors2,childerrors2])

        # sorting all the candidates by error
        candidateerrorsinds=candidate_errors.argsort()
        candidate_errors=candidate_errors[candidateerrorsinds[::1]]
        candidate_errors1=candidate_errors1[candidateerrorsinds[::1]]
        candidate_errors2=candidate_errors2[candidateerrorsinds[::1]]
        candidates=candidates[candidateerrorsinds[::1]]

        # setting the probability and choosing the indices
        # candidate_prob=gen_parent_probabilities(pop_size*2)
        # chosenindices=np.random.choice(np.arange(0,2*pop_size),pop_size, replace=False,p=candidate_prob)

        # set population for the next iteration 

        for i in range(pop_size):
            population[i]=candidates[i]
            parenterrors[i]=candidate_errors[i]
            parenterrors1[i]=candidate_errors1[i]
            parenterrors2[i]=candidate_errors2[i]

        # set the send array by choosing the minimum from all the candidates NOTE: it may not be selected in the new population 
        if(min_error==-1 or min_error>candidate_errors[0]):
            to_send=candidates[0]
            min_error=candidate_errors[0]
            min_error1=candidate_errors1[0]
            min_error2=candidate_errors2[0]
        print("-------------------------------------------------------------------------------\n")
        print("Min error = ", min_error,"\n\n")
        print("Min error1 = ", min_error1,"\n\n")
        print("Min error2 = ", min_error2,"\n\n")

        if(min_error<40000000):
            print("sending\n\n"+str(to_send)+"\n\nwas it successfully submitted?", server.submit(key,to_send.tolist()))
            
    return to_send

to_send=main()
print("sending\n\n"+str(to_send)+"\n\nwas it successfully submitted?", server.submit(key,to_send.tolist()))
print("Code finished")
print("-------------------------------------------------------------------------------\n\n")