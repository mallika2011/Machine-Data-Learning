import cvxpy as cp
import numpy as np

x = cp.Variable(shape=(9,1), name="x")
A = np.array([[1,1,0,0,0,0,0,0,0],[-1,0,1,0,0,0,0,0,0],[0,-1,0,1,0.5,0.2,0,0,0],[0,0,0,-1,0,0,1,0,0],[0,0,0,0,0,-0.2,0,1,0],[0,0,0,0,-0.5,0,0,0,1]])
alpha = np.array([0.1,0.1,0.1,0.1,0.1,0.5])
r=np.array([0,0,5,1,1,1,-10,50,60])

alpha.shape=(6,1)

print(alpha)

constraints = [x>=0,cp.matmul(A, x) <= alpha, cp.matmul(A, x) >= alpha]
objective = cp.Maximize(cp.sum(cp.matmul(r,x), axis=0))
problem = cp.Problem(objective, constraints)

solution = problem.solve()
print(solution)

print(x.value)