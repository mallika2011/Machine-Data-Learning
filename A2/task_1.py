
def check(health1,arrows1,stamina1,health2,arrows2,stamina2,dh,da,ds):
    if (dh==health1-health2) and (da==arrows1-arrows2) and (ds==stamina1-stamina2):
        return 1
    else:
         return 0

def shoot(h1,a1,s1,h2,a2,s2):

    #no arrows or no health
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
