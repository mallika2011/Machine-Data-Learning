import cvxpy as cp
import numpy as np

x = cp.Variable(shape=(2,1), name="x")
A = np.array([[4,3],[-3,4]])

constraints = [cp.matmul(A, x) <= 12, x<=2, x>=0]
objective = cp.Maximize(cp.sum(x, axis=0))
problem = cp.Problem(objective, constraints)

solution = problem.solve()
print(solution)

print(x.value)