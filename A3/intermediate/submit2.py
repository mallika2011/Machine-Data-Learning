# import tester as server
import client_moodle as server
key = '847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'

lst=[]
# creating an empty list
lst1 =input().split()
lst2 =input().split()
lst3 =input().split()
for i in range(0,4):
    lst.append(float(lst1[i]))
    
for i in range(0,4):
    lst.append(float(lst2[i]))
    
for i in range(0,3):
    lst.append(float(lst3[i]))
    

print(lst)
print("sending\n\n"+str(lst)+"\n\nwas it successfully submitted?", server.submit(key,lst))
print("Code finished")
print("-------------------------------------------------------------------------------\n\n")
