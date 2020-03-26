import numpy as np
import tester as server
# import client_moodle as server
import random

team_name = "team_62"  # for our reference
MAX_DEG = 11  # number of features
key = '847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'
ranger = 10
pc = 0.2
pop_size = 30
select_sure = 5
cross_n = int(pop_size/2)
iter = 100


def mutation(vector, index=-1, mut_prob=0.2):  # TODO: Changed mutate_prob to 0.2
    if index == -1:
        index = random.randint(0, MAX_DEG-1)

    parity = np.random.choice((0, 1), p=[1-mut_prob, mut_prob])

    if parity == 1:
        vector[index] = random.uniform(-ranger, ranger)
    return vector


def mutateall(temp):
    vector = np.copy(temp)
    for i in range(len(vector)):
        # TODO: MUTATE WITH RANGES
        # lo=max(-ranger,vector[i]-2)
        # hi=min(ranger,vector[i]+2)
        lo = max(-ranger, vector[i]+vector[i]*random.uniform(0, 1))
        hi = min(ranger, vector[i]-vector[i]*random.uniform(0, 1))
        vector[i] = np.random.choice(
            [random.uniform(lo, hi), vector[i]], p=[0.95, 0.05])
    return vector


def crossover(vector1, vector2, index=-1):
    send1 = []
    send2 = []

    index = random.randint(0, MAX_DEG-1)

    for i in range(MAX_DEG):
        parity = random.randint(0, 1)
        if parity == 1:
            send1.append(vector1[i])
            send2.append(vector2[i])
        else:
            send1.append(vector2[i])
            send2.append(vector1[i])

    return mutation(send1), mutation(send2)


def gen_parent_probabilities(size):
    parentprobalities = np.zeros(size)
    for j in range(size-1):
        parentprobalities[j] = ((1-pc)**j)*pc
    parentprobalities[size-1] = ((1-pc)**(size-1))
    return parentprobalities


def crossover_select(parentprobalities):
    parents = []
    parents = np.random.choice(
        np.arange(0, pop_size), 2, replace=False, p=parentprobalities)
    return parents

def crossover_select2(parenterrors, num):
    return random.sample(range(pop_size),num)


def check_match(vector1, vector2):
    # return 1 if match
    count = 0
    for i in range(MAX_DEG):
        if (abs(vector1[i]-vector2[i]) > 0.5):
            count += 1
    if count >= 5:
        return 0
    else:
        return 1


def main():
    print("PC: ", pc, " POP_SIZE: ", pop_size,
          " ITER : ", iter, "Stop : ", "50")

    vector_og = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -
                 6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
    # vector_og=[-9.78736351e+00 ,-6.30079234e+00 ,-5.86904268e+00 , 4.93390314e-02,3.81084816e-02 , 8.13236610e-05, -6.01876916e-05, -1.25158557e-07,3.48409638e-08,  4.16149250e-11, -6.73242018e-12]
    to_send = [-20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20]
    min_error = -1
    min_error1 = -1
    min_error2 = -1

    parenterrors = np.zeros(pop_size)
    parenterrors1 = np.zeros(pop_size)
    parenterrors2 = np.zeros(pop_size)
    parentprobalities = np.zeros(pop_size)
    population = np.zeros((pop_size, MAX_DEG))

    # generate the population
    for i in range(pop_size):
        temp = np.copy(vector_og)
        population[i] = mutateall(temp)

    # generate errors for each individual in the population
    for j in range(pop_size):
        # passing a list to the get_errors function
        temp = population[j].tolist()
        err = server.get_errors(key, temp)

        # adding the two errors and storing in parenterror
        parenterrors[j] = (err[0]+err[1])
        parenterrors1[j] = (err[0])
        parenterrors2[j] = (err[1])

    # have to change this to a while loop with appropriate condition later
    for iter_num in range(iter):

        print("\n\n\n\n********"+str(iter_num)+"*********")

        parenerrorsinds = parenterrors.argsort()
        parenterrors = parenterrors[parenerrorsinds[::1]]
        parenterrors1 = parenterrors1[parenerrorsinds[::1]]
        parenterrors2 = parenterrors2[parenerrorsinds[::1]]
        population = population[parenerrorsinds[::1]]

        # debug statements
        for j in range(pop_size):
            print("person " + str(j)+" error " + str(parenterrors[j]))
            print("person " + str(j)+" error " + str(parenterrors1[j]))
            print("person " + str(j)+" error " + str(parenterrors2[j]))
            print("\tvalues"+str(population[j])+"\n\n")

        # Assign probabilities to the population
        parentprobalities = gen_parent_probabilities(pop_size)

        child_population = np.zeros((pop_size, MAX_DEG))
        new_iter = 0
        
        while(new_iter < pop_size):

            #TODO: WE MAY HAVE TO CHOOSE BETWEEN THESE TWO OPTIONS
            arr = crossover_select(parentprobalities)
            
            #TODO: Select randomly among top k parents  (For now k =10) 
            # arr = crossover_select2(parenterrors, 10)

            # Sending parents for crossover
            temp = crossover(population[arr[0]], population[arr[1]])
            if temp[0] == population[arr[0]].tolist() or temp[1] == population[arr[0]].tolist() or temp[0] == population[arr[1]].tolist() or temp[1] == population[arr[1]].tolist():
                # print("repeated")
                # print("first", temp[0])
                # print("Second", temp[1])
                continue

            child_population[new_iter] = temp[0]
            new_iter += 1

            child_population[new_iter] = temp[1]
            new_iter += 1

        childerrors = np.zeros(pop_size)
        childerrors1 = np.zeros(pop_size)
        childerrors2 = np.zeros(pop_size)

        # generate errors for each child
        for j in range(pop_size):
            temp = child_population[j].tolist()
            err = server.get_errors(key, temp)

            # adding the two errors and storing in parenterror
            childerrors[j] = (err[0]+err[1])
            childerrors1[j] = (err[0])
            childerrors2[j] = (err[1])

        #TODO: Select the best select_sure number of parents and chilren [select these many parents and children for sure]

        for j in range (select_sure):
            #Leaving the parent population untouched
            population[j+select_sure] = child_population[j]
            parenterrors[j+select_sure] = childerrors[j]
            parenterrors1[j+select_sure] = childerrors1[j]
            parenterrors2[j+select_sure] = childerrors2[j]

        

        # combining parents and children into one array
        #TODO: Concatenating remaining parents and children and selecting from them
        candidates = np.concatenate([population[select_sure:], child_population[select_sure:]])
        candidate_errors = np.concatenate([parenterrors[select_sure:], childerrors[select_sure:]])
        candidate_errors1 = np.concatenate([parenterrors1[select_sure:], childerrors1[select_sure:]])
        candidate_errors2 = np.concatenate([parenterrors2[select_sure:], childerrors2[select_sure:]])

        # sorting all the candidates by error
        candidate_errors_inds = candidate_errors.argsort()
        candidate_errors = candidate_errors[candidate_errors_inds[::1]]
        candidate_errors1 = candidate_errors1[candidate_errors_inds[::1]]
        candidate_errors2 = candidate_errors2[candidate_errors_inds[::1]]
        candidates = candidates[candidate_errors_inds[::1]]

        #TODO: Select the best popsize - 2*(select_sure)
        cand_iter = 0

        while(cand_iter < pop_size - 2*select_sure):
            population[cand_iter] = candidates[cand_iter]
            parenterrors[cand_iter] = candidate_errors[cand_iter]
            parenterrors1[cand_iter] = candidate_errors1[cand_iter]
            parenterrors2[cand_iter] = candidate_errors2[cand_iter]
            cand_iter+=1


        # set the send array by choosing the minimum from all the candidates NOTE: it may not be selected in the new population
        if(min_error == -1 or min_error > candidate_errors[0]):
            to_send = candidates[0]
            min_error = candidate_errors[0]
            min_error1 = candidate_errors1[0]
            min_error2 = candidate_errors2[0]

        else:
            print("no improvement!!!")
        print("-------------------------------------------------------------------------------\n")
        print("Min error = ", min_error, "\n\n")
        print("Min error1 = ", min_error1, "\n\n")
        print("Min error2 = ", min_error2, "\n\n")

        # if(min_error<40000000):
        # print("sending\n\n"+str(to_send)+"\n\nwas it successfully submitted?", server.submit(key,to_send.tolist()))

    return to_send


to_send = main()
print("sending\n\n"+str(to_send)+"\n\nwas it successfully submitted?",
      server.submit(key, to_send.tolist()))
print("Code finished")
print("-------------------------------------------------------------------------------\n\n")
