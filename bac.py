import numpy as np
from scipy.optimize import linprog


class MIPProblem:
    def __init__(self, c, A_ub, b_ub, A_eq, b_eq, bounds, int_vars):
        self.c = c  # Objective function coefficients
        self.A_ub = A_ub  # Inequality constraint matrix
        self.b_ub = b_ub  # Right-hand side of inequality constraints
        self.A_eq = A_eq  # Equality constraint matrix
        self.b_eq = b_eq  # Right-hand side of equality constraints
        self.bounds = bounds  # Variable bounds
        self.int_vars = int_vars  # Indices of integer variables

class Node:
    def __init__(self, bounds):
        self.bounds = bounds  # This should be a list of tuples, e.g., [(0, None), (0, None)]
        self.solution = None
        self.objective = None

def solve_lp(c, A_ub, b_ub, A_eq, b_eq, bounds):
    res = linprog(-c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    return res.x if res.success else None


def is_integer(x, tol=1e-6):
    """
    Checks if a solution is integer-feasible within a tolerance.

    Args:
    x: Solution vector
    tol: Tolerance for integer feasibility

    Returns:
    bool: True if x is integer-feasible, False otherwise
    """
    return np.all(np.abs(x - np.round(x)) < tol)

def generate_cut(x, A, b):
    """
    Generates a simple Gomory cut.
    This is a basic implementation and could be expanded with more sophisticated cutting plane techniques.

    Args:
    x: Current LP solution
    A: Constraint matrix
    b: Right-hand side of constraints

    Returns:
    cut: Coefficients of the cut
    rhs: Right-hand side of the cut
    """
    row = np.argmax(np.abs(x - np.round(x)))  # Find the most fractional variable
    f = x[row] - np.floor(x[row])  # Fractional part
    cut = np.floor(A[row]) - A[row]
    cut[cut < 0] = 0  # Ensure non-negativity
    rhs = np.floor(b[row]) - f
    return cut, rhs

def branch_and_cut(problem, node):
    c, A_ub, b_ub, A_eq, b_eq, bounds = problem.c, problem.A_ub, problem.b_ub, problem.A_eq, problem.b_eq, problem.bounds

    # Apply node bounds
    if node.bounds:
        bounds = [
            (
                max(node.bounds[i][0], bounds[i][0]) if node.bounds[i][0] is not None and bounds[i][0] is not None else node.bounds[i][0] or bounds[i][0],
                min(node.bounds[i][1], bounds[i][1]) if node.bounds[i][1] is not None and bounds[i][1] is not None else node.bounds[i][1] or bounds[i][1]
            )
            for i in range(len(bounds))
        ]

    # Solve LP relaxation
    x = solve_lp(c, A_ub, b_ub, A_eq, b_eq, bounds)
    
    if x is None:
        return None, float('-inf')  # Infeasible
    
    obj = np.dot(c, x)  # Calculate objective value
    
    # Check if solution is integer-feasible
    if is_integer(x[problem.int_vars]):
        return x, obj
    
    # Generate and add cut
    cut, rhs = generate_cut(x, A_ub, b_ub)
    A_ub = np.vstack((A_ub, cut))
    b_ub = np.append(b_ub, rhs)
    
    # Solve again with the new cut
    x = solve_lp(c, A_ub, b_ub, A_eq, b_eq, bounds)
    
    if x is None or is_integer(x[problem.int_vars]):
        return x, np.dot(c, x) if x is not None else float('-inf')
    
    # Branch on the most fractional variable
    var = problem.int_vars[np.argmax(np.abs(x[problem.int_vars] - np.round(x[problem.int_vars])))]
    
    # Create left branch (x_var <= floor(x_var))
    A_ub_left = np.vstack((A_ub, np.zeros(len(c))))
    A_ub_left[-1, var] = 1
    b_ub_left = np.append(b_ub, np.floor(x[var]))
    left_problem = MIPProblem(c, A_ub_left, b_ub_left, A_eq, b_eq, bounds, problem.int_vars)
    x_left, obj_left = branch_and_cut(left_problem, Node(bounds))
    
    # Create right branch (x_var >= ceil(x_var))
    A_ub_right = np.vstack((A_ub, np.zeros(len(c))))
    A_ub_right[-1, var] = -1
    b_ub_right = np.append(b_ub, -np.ceil(x[var]))
    right_problem = MIPProblem(c, A_ub_right, b_ub_right, A_eq, b_eq, bounds, problem.int_vars)
    x_right, obj_right = branch_and_cut(right_problem, Node(bounds))
    
    # Return the better of the two branches
    if obj_left > obj_right:
        return x_left, obj_left
    else:
        return x_right, obj_right
    
def solve_mip(c, A_ub, b_ub, A_eq, b_eq, bounds, int_vars, minimize=True):
    if not minimize:
        c = -c

    problem = MIPProblem(c, A_ub, b_ub, A_eq, b_eq, bounds, int_vars)
    root = Node(bounds)  # Pass the bounds here
    x, obj = branch_and_cut(problem, root)

    if not minimize:
        obj = -obj

    return x, obj


    
    
# if __name__ == "__main__":
#     c = np.array([3, 2])
#     A_ub = np.array([[2, 1], [1, 3]])
#     b_ub = np.array([8, 8])
#     A_eq = np.array([[1, 1]])
#     b_eq = np.array([5])
#     bounds = [(0, None), (0, None)]  # x >= 0, y >= 0
#     int_vars = [1, 1]  # Both variables are integer

#     x_min, obj_min = solve_mip(c, A_ub, b_ub, A_eq, b_eq, bounds, int_vars, minimize=True)
#     print(f"Minimization - Optimal solution: {x_min}")
#     print(f"Minimization - Optimal objective: {obj_min}")
