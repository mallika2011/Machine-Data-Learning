import numpy as np
# import tester as server
import client_moodle as server
import random

team_name = "team_62"  # for our reference
MAX_DEG = 11  # number of features
key = '847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'
ranger = 10
pc = 0.2
pop_size = 30
select_sure = 5
cross_select_from = 10
cross_n = int(pop_size/2)
iter = 30
prob_mut_cross=0.5
mutate_range=0.1

# def mutation(vector, index=-1, mut_prob=0.2):  # TODO: Changed mutate_prob to 0.2
#     if index == -1:
#         index = random.randint(0, MAX_DEG-1)

#     parity = np.random.choice((0, 1), p=[1-mut_prob, mut_prob])

#     if parity == 1:
#         vector[index] = random.uniform(-ranger, ranger)
#     return vector


def mutateall(temp,prob):
    vector = np.copy(temp)
    for i in range(len(vector)):
        fact=random.uniform(-mutate_range, mutate_range)
        vector[i] = np.random.choice([vector[i]*(fact+1), vector[i]], p=[prob,1-prob])
        if(vector[i]<-10) :
            vector[i]=-10
        elif(vector[i]>10) :
            vector[i]=10
    
    return vector


# def crossover(vector1, vector2, index=-1):
#     send1 = []
#     send2 = []

#     index = random.randint(0, MAX_DEG-1)

#     for i in range(MAX_DEG):
#         parity = random.randint(0, 1)
#         if parity == 1:
#             send1.append(vector1[i])
#             send2.append(vector2[i])
#         else:
#             send1.append(vector2[i])
#             send2.append(vector1[i])

#     return mutation(send1), mutation(send2)
def crossover(vector1, vector2, index=-1):
    send1 = vector1.tolist()
    send2 = vector2.tolist()

    a = np.random.choice(np.arange(0, 11), 5, replace=False)

    for i in a.tolist():
        send1[i] = np.copy(vector2[i])
        send2[i] = np.copy(vector1[i])

    return mutateall(send1,prob_mut_cross), mutateall(send2,prob_mut_cross)


# def gen_parent_probabilities(size):
#     parentprobalities = np.zeros(size)
#     for j in range(size-1):
#         parentprobalities[j] = ((1-pc)**j)*pc
#     parentprobalities[size-1] = ((1-pc)**(size-1))
#     return parentprobalities


# def crossover_select(parentprobalities):
#     parents = []
#     parents = np.random.choice(
#         np.arange(0, pop_size), 2, replace=False, p=parentprobalities)
#     return parents


def crossover_select2(parenterrors, num):
    return random.sample(range(num), 2)


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
    print("pop_size:", pop_size, "iter:", iter, "cross_select_from",cross_select_from)
    print("select_sure",select_sure,"prob_mut_cross",prob_mut_cross,"mutate_range",mutate_range)

    vector_og = [-1e-19, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -
                 6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
    to_send = [-20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20]
    min_error = -1
    min_error1 = -1
    min_error2 = -1

    parenterrors = np.zeros(pop_size)
    parenterrors1 = np.zeros(pop_size)
    parenterrors2 = np.zeros(pop_size)
    # parentprobalities = np.zeros(pop_size)
    population = np.zeros((pop_size, MAX_DEG))

    # generate the population
    for i in range(pop_size):
        temp = np.copy(vector_og)
        population[i] = np.copy(mutateall(temp,0.85))

    # generate errors for each individual in the population
    for j in range(pop_size):
        # passing a list to the get_errors function
        temp = population[j].tolist()
        err = server.get_errors(key, temp)

        # adding the two errors and storing in parenterror
        parenterrors[j] = np.copy((err[0]+err[1]))
        parenterrors1[j] = np.copy((err[0]))
        parenterrors2[j] = np.copy((err[1]))

    # have to change this to a while loop with appropriate condition later
    for iter_num in range(iter):

        print("\n\n\n\n********"+str(iter_num)+"*********")

        parenerrorsinds = parenterrors.argsort()
        parenterrors = np.copy(parenterrors[parenerrorsinds[::1]])
        parenterrors1 = np.copy(parenterrors1[parenerrorsinds[::1]])
        parenterrors2 = np.copy(parenterrors2[parenerrorsinds[::1]])
        population = np.copy(population[parenerrorsinds[::1]])

        # debug statements
        for j in range(pop_size):
            print("person " + str(j)+" errorfunc" + str(parenterrors[j]))
            print("person " + str(j)+" error1" + str(parenterrors1[j]))
            print("person " + str(j)+" error2" + str(parenterrors2[j]))
            print("\tvalues"+str(population[j])+"\n\n")

        # Assign probabilities to the population
        # parentprobalities = gen_parent_probabilities(pop_size)

        child_population = np.zeros((pop_size, MAX_DEG))
        new_iter = 0

        while(new_iter < pop_size):

            # TODO: WE MAY HAVE TO CHOOSE BETWEEN THESE TWO OPTIONS
            # arr = crossover_select(parentprobalities)

            # TODO: Select randomly among top k parents  (For now k =10)
            arr = crossover_select2(parenterrors, cross_select_from)

            # Sending parents for crossover
            temp = crossover(population[arr[0]], population[arr[1]])
            if temp[0].tolist() == population[arr[0]].tolist() or temp[1].tolist() == population[arr[0]].tolist() or temp[0].tolist() == population[arr[1]].tolist() or temp[1].tolist() == population[arr[1]].tolist():
                # print("repeated")
                # print("first", temp[0])
                # print("Second", temp[1])
                continue

            child_population[new_iter] = np.copy(temp[0])
            new_iter += 1

            child_population[new_iter] = np.copy(temp[1])
            new_iter += 1

        childerrors = np.zeros(pop_size)
        childerrors1 = np.zeros(pop_size)
        childerrors2 = np.zeros(pop_size)

        # generate errors for each child
        for j in range(pop_size):
            temp = child_population[j].tolist()
            err = server.get_errors(key, temp)

            # adding the two errors and storing in parenterror
            childerrors[j] = np.copy((err[0]+err[1]))
            childerrors1[j] = np.copy((err[0]))
            childerrors2[j] = np.copy((err[1]))

        # Sort children
        childinds = np.copy(childerrors.argsort())
        childerrors = np.copy(childerrors[childinds[::1]])
        childerrors1 = np.copy(childerrors1[childinds[::1]])
        childerrors2 = np.copy(childerrors2[childinds[::1]])
        child_population = np.copy(child_population[childinds[::1]])
        # TODO: Select the best select_sure number of parents and chilren [select these many parents and children for sure]

        # now the children are sorted and stored in child and parents are sorted in population
        # we will now create a tempbank array to store top k parents, top k childs and rest being sorted taking from the top
        tempbankerr = np.zeros(pop_size)
        tempbankerr1 = np.zeros(pop_size)
        tempbankerr2 = np.zeros(pop_size)
        tempbank= np.zeros((pop_size, MAX_DEG))
        
        for j in range(select_sure):
            
            #choosing the top jth parent and putting in the array
            tempbank[j]=np.copy(population[j])
            tempbankerr[j]=np.copy(parenterrors[j])
            tempbankerr1[j]=np.copy(parenterrors1[j])
            tempbankerr2[j]=np.copy(parenterrors2[j])
            
            #choosing the top jth child and putting it into the array 
            tempbank[j+select_sure]=np.copy(child_population[j])
            tempbankerr[j+select_sure]=np.copy(childerrors[j])
            tempbankerr1[j+select_sure]=np.copy(childerrors1[j])
            tempbankerr2[j+select_sure]=np.copy(childerrors2[j])

        # combining parents and children into one array
        # TODO: Concatenating remaining parents and children and selecting from them
        candidates = np.copy(np.concatenate([population[select_sure:], child_population[select_sure:]]))
        candidate_errors = np.copy(np.concatenate([parenterrors[select_sure:], childerrors[select_sure:]]))
        candidate_errors1 = np.copy(np.concatenate([parenterrors1[select_sure:], childerrors1[select_sure:]]))
        candidate_errors2 = np.copy(np.concatenate([parenterrors2[select_sure:], childerrors2[select_sure:]]))

        # sorting all the candidates by error
        candidate_errors_inds = candidate_errors.argsort()
        candidate_errors = np.copy(candidate_errors[candidate_errors_inds[::1]])
        candidate_errors1 = np.copy(candidate_errors1[candidate_errors_inds[::1]])
        candidate_errors2 = np.copy(candidate_errors2[candidate_errors_inds[::1]])
        candidates = np.copy(candidates[candidate_errors_inds[::1]])

        # TODO: Select the best popsize - 2*(select_sure)
        cand_iter = 0

        while(cand_iter + 2*select_sure < pop_size):
            tempbank[cand_iter+2*select_sure] = np.copy(candidates[cand_iter])
            tempbankerr[cand_iter+2*select_sure] = np.copy(candidate_errors[cand_iter])
            tempbankerr1[cand_iter+2*select_sure] = np.copy(candidate_errors1[cand_iter])
            tempbankerr2[cand_iter+2*select_sure] = np.copy(candidate_errors2[cand_iter])
            cand_iter += 1


        #now setting the next population
        population=np.copy(tempbank)
        parenterrors=np.copy(tempbankerr)
        parenterrors1=np.copy(tempbankerr1)
        parenterrors2=np.copy(tempbankerr2)

        #we will now sort before updating min_error
        parenerrorsinds = parenterrors.argsort()
        parenterrors = np.copy(parenterrors[parenerrorsinds[::1]])
        parenterrors1 = np.copy(parenterrors1[parenerrorsinds[::1]])
        parenterrors2 = np.copy(parenterrors2[parenerrorsinds[::1]])
        population = np.copy(population[parenerrorsinds[::1]])


        if(min_error == -1 or min_error > parenterrors[0]):
            to_send = np.copy(population[0])
            min_error = np.copy(parenterrors[0])
            min_error1 = np.copy(parenterrors1[0])
            min_error2 = np.copy(parenterrors2[0])
            nochange=0

        else:
            print("no improvement!!!")
            nochange+=1
            if(nochange>10):
                print("Breaking")
                print("-------------------------------------------------------------------------------\n")
                print("Min error = ", min_error, "\n\n")
                print("Min error1 = ", min_error1, "\n\n")
                print("Min error2 = ", min_error2, "\n\n")
                break
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
