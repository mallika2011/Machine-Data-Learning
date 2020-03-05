import numpy as np

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

def mapactions(ac):
    if ac==0:
        return "shoot"
    elif ac==1:
        return "dodge"
    elif ac==2:
        return "recharge"

def callaction(ac,h1,a1,s1,h2,a2,s2):

    if ac==0:
        return shoot(h1,a1,s1,h2,a2,s2)

    elif ac==1:
        return dodge(h1,a1,s1,h2,a2,s2)

    elif ac==2:
        return recharge(h1,a1,s1,h2,a2,s2)


penalty=[-20,-20,-20] #step cost
happyreward=10
gamma=0.99
delta=0.001

actionsnum=3 #shoot,dodge,recharge
health=5 #mult by 25
arrows=4
stamina=3 #mult by 50

states=np.zeros((health,arrows,stamina))
actions=np.zeros((health,arrows,stamina))

#numpy.copyto(dst, src)
deltacheck=100000000

while(deltacheck>delta):

    temparray=np.zeros((health,arrows,stamina))
    temparray[:]=-100000000
    deltacheck=-100000000
    actions[:]=-1

    for h1 in range(0,health):
        for a1 in range(0,arrows):
            for s1 in range(0,stamina):
                #for each state

                for ac in range(0,actionsnum):
                    # for each action
                    temp=penalty[ac]
                    for h2 in range(0,health):
                        for a2 in range(0,arrows):
                            for s2 in range(0,stamina):
                                temp+=callaction(ac,h1,a1,s1,h2,a2,s2)*states[h2,a2,s2]

                    if(temp>temparray[h1,a1,s1]):
                        temparray[h1,a1,s1]=temp

                if(abs(temparray[h1,a1,s1]-states[h1,a1,s1])>deltacheck):
                    deltacheck=abs(temparray[h1,a1,s1]-states[h1,a1,s1])
                    actions[h1,a1,s1]=ac

    np.copyto(states, temparray)
