import cvxpy as cp
import numpy as np
import json
import os
import sys

def check(health1,arrows1,stamina1,health2,arrows2,stamina2,dh,da,ds):
    if (dh==health1-health2) and (da==arrows1-arrows2) and (ds==stamina1-stamina2):
        return 1
    else:
        return 0


def shoot(h1,a1,s1,h2,a2,s2):

    #no arrows or no stamina
    if a1==0 or s1==0:
        return check(h1,a1,s1,h2,a2,s2,0,0,0)

    #misses MD
    elif check(h1,a1,s1,h2,a2,s2,0,1,50):
        return 0.5

    #hits MD
    elif check(h1,a1,s1,h2,a2,s2,25,1,50):
        return 0.5

    else:
        return 0

def dodge (h1,a1,s1,h2,a2,s2):

    #zero stamina
    if s1==0:
        return 0

    #stamina is 50
    elif s1==50:

        #arrows already full
        if a1==3 and check(h1,a1,s1,h2,a2,s2,0,0,50):
            return 1

        #unsuccessful arrow pickup
        elif check(h1,a1,s1,h2,a2,s2,0,0,50):
            return 0.2

        #successful arrow pickup
        elif check(h1,a1,s1,h2,a2,s2,0,-1,50):
            return 0.8


    #stamina is 100
    elif s1==100:

        #3 arrows
        if(a1==3):

            #lose 50 stamins
            if check(h1,a1,s1,h2,a2,s2,0,0,50):
                return 0.8

            #lose 100 stamina
            elif check(h1,a1,s1,h2,a2,s2,0,0,100):
                return 0.2


        #successful arrow pickup, 50 stamina loss
        elif check(h1,a1,s1,h2,a2,s2,0,-1,50):
            return 0.8*0.8

        #unsuccessful arrow pickup, 50 stamina loss
        elif check(h1,a1,s1,h2,a2,s2,0,0,50):
            return 0.2*0.8

        #successful arrow pickup, 100 stamina loss
        elif check(h1,a1,s1,h2,a2,s2,0,-1,100):
            return 0.8*0.2

        #unsuccessful arrow pickup, 100 stamina loss
        elif check(h1,a1,s1,h2,a2,s2,0,0,100):
            return 0.2*0.2

    return 0

def recharge (h1,a1,s1,h2,a2,s2):

    #stamina is 100
    if(s1==100):

        if check(h1,a1,s1,h2,a2,s2,0,0,0)==1:
            return 1
        else:
            return 0

    #stamina not 100
    else:
        if check(h1,a1,s1,h2,a2,s2,0,0,-50): #since stamina increase therefore old-new = -50
            return 0.8
        elif check(h1,a1,s1,h2,a2,s2,0,0,0):
            return 0.2

        else:
            return 0

def numtocomp(num):
    s=num%3
    a=(int(num/3))%4
    h=(int(num/12))%5
    
    return h,a,s

def comptonum(h,a,s):
    num=h*12+a*3+s
    return num
    
def mapactions(ac):
    if ac==0:
        return "SHOOT"
    elif ac==1:
        return "DODGE"
    elif ac==2:
        return "RECHARGE"
    elif ac==3:
        return "NOOP"
    else:
        return "ERROR"

def callaction(ac,h1,a1,s1,h2,a2,s2):

    if ac==0:
        return shoot(h1,a1,s1,h2,a2,s2)

    elif ac==1:
        return dodge(h1,a1,s1,h2,a2,s2)

    elif ac==2:
        return recharge(h1,a1,s1,h2,a2,s2)

    elif ac==3:
        return 0

actionsnum=4 #shoot,dodge,recharge,noop
health=5 #mult by 25
arrows=4
stamina=3 #mult by 50
states = 60 

columns=0 # every time we find an action we can add a column
r=[] #rewards array
reward = -5
actions=[]
a=[]
for h1 in range(0,health):
    for a1 in range(0,arrows):
        for s1 in range(0,stamina):
            #for each state

            #storing the actions possible
            tempac=[]
            for ac in range(0,actionsnum):
                # for each action

                #noop conditions
                if (ac!=3 and h1==0) or (ac==3 and h1!=0):
                    continue

                #conditions for skipping actions
                if (a1==0 and ac==0) or (s1==0 and ac==0) or (s1==0 and ac==1) or (s1==2 and ac==2):
                    continue
                
                #reward =0 for terminal, reward = -5 for others
                if(h1==0):
                    r.append(0)
                else:
                    r.append(reward)
                
                columns+=1
                # print(columns, ". In state ", h1,a1,s1,"taking action ", mapactions(ac))
                tempac.append(ac)
                newcol=[]
                out=0
                #making the column, we are iterating 0 to 60
                for h2 in range(0,health):
                    for a2 in range(0,arrows):
                        for s2 in range(0,stamina):
                    
                            if check(h1,a1,s1,h2,a2,s2,0,0,0)==1: #selfloop
                                newcol.append(0)
                                continue

                            #callaction returns probalilty of action causing inflow into h2,a2,s2 
                            #and outflow from h1,a1,s1.
                            prob=round(callaction(ac,h1*25,a1,s1*50,h2*25,a2,s2*50),3)
                            out+=prob
                            newcol.append(-prob) #inflow

                #exception case oof noop    
                if ac==3:
                    out=1

                #now adding the outflow of        
                newcol[comptonum(h1,a1,s1)]=out

                a.append(newcol)

            #appending to the actions lis
            actions.append(tempac)

# a and actions are prepared as list of lists
# number of columns is stored in column

# print(r)

#initial probabilities
alpha=[0]*60
alpha[comptonum(4,3,2)]=1 #probability of starting here is 1


#create the json object and add these lists to the json before they are used in cvxpy
send = {}


#Fields to include in the JSON : 

#The A matrix - a
a=np.array(a)
a=np.transpose(a)
send["a"] = a.tolist()
# print(a)
# print(a.shape)

send["r"]= r
send["alpha"] = alpha

#The R array - r
r=np.array(r)
# print("\n",r)

#The alpha array - alpha
alpha=np.array(alpha)
alpha.shape=(states,1)
# print("\n",alpha)


x = cp.Variable(shape=(columns,1), name="x")


constraints = [cp.matmul(a, x) == alpha, x>=0]
objective = cp.Maximize(cp.sum(cp.matmul(r,x), axis=0))
problem = cp.Problem(objective, constraints)

solution = problem.solve()

x_send=[]

for it in x.value:
    x_send.append(it[0])    

send["x"] = x_send

policy=[]
index=0
st = 0

for ac in actions:
    #each element is an array
    # print(ac)
    num=index
    max_value = x_send[index]
    ac_taken=ac[0]
    allx=[]
    for i in range(len(ac)):
        allx.append(x_send[num])
        if x_send[num]>=max_value:
            max_value = x_send[num]
            ac_taken=ac[i]
        num+=1
    index+=len(ac)
    h,a,s=numtocomp(st)
    st+=1
    # print("\nx's:",allx)
    # print("actions",ac)
    haslis=[]
    haslis.append(h)
    haslis.append(a)
    haslis.append(s)
    temp=[]
    temp.append(haslis)
    temp.append(mapactions(ac_taken))
    policy.append(temp)
    # print(h,a,s, mapactions(ac_taken),ac_taken,ac,allx)

send["policy"] = policy
send["objective"]=solution


# Dumping the JSON object into the directory

# original = sys.stdout
# os.mkdir("./outputs")
# sys.stdout = original

# file_object = open("outputs/output.json", 'w')
# json.dump(send, file_object)


filename="./outputs/output.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as file_object:
    json.dump(send,file_object)