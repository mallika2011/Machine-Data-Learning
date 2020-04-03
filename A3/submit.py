# import tester as server
import client_moodle as server
key = '847FWwSwTAxKTPvfixjzNnxbeudiTzJ9psoVIdUxqehtQ5efNo'

# creating an empty list
lst =input().split()
print(lst)
for i in range(0,11):
    lst[i]=float(lst[i])
print("sending\n\n"+str(lst)+"\n\nwas it successfully submitted?", server.submit(key,lst))
print("Code finished")
print("-------------------------------------------------------------------------------\n\n")
