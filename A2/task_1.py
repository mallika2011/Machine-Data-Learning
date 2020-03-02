
def check(health1,arrows1,stamina1,health2,arrows2,stamina2,dh,da,ds):
    if (dh==health1-health2) and (da==arrows1-arrows2) and (ds==stamina1-stamina2):
        return 1
    else:
         return 0

def shoot(h1,a1,s1,h2,a2,s2):

    if a1==0 or s1==0:
        return check(h1,a1,s1,h2,a2,s2,0,0,0)

    elif check(h1,a1,s1,h2,a2,s2,0,1,50):
        return 0.5

    elif check(h1,a1,s1,h2,a2,s2,25,1,50):
        return 0.5

    else:
        return 0


def dodge (h1,a1,s1,h2,a2,s2):
    
