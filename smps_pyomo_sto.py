import pyomo.environ as pyo
import pyomo.opt as pyopt
from pyomo.core import Suffix

def read_cor_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_servers = 5
    num_clients = 25
    fixed_costs = [0] * num_servers
    revenues = {}
    capacity = 188

    for line in lines:
        parts = line.split()
        if len(parts) >= 4 and parts[0].startswith('x_') and parts[1] == 'obj':
            server = int(parts[0].split('_')[1]) - 1  # Adjust for 0-based indexing
            fixed_costs[server] = float(parts[2])
        elif len(parts) >= 5 and parts[0].startswith('y_') and parts[2] == 'obj':
            client = int(parts[0].split('_')[1]) - 1  # Adjust for 0-based indexing
            server = int(parts[0].split('_')[2]) - 1  # Adjust for 0-based indexing
            revenue = -float(parts[3])  # Negate because we're maximizing
            revenues[(client, server)] = revenue

    return num_servers, num_clients, fixed_costs, revenues, capacity

def read_sto_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    scenarios = {}
    current_scenario = None
    scenario_prob = None

    for line in lines:
        parts = line.split()
        if len(parts) >= 4 and parts[0] == 'SC':
            current_scenario = parts[1]
            scenario_prob = float(parts[3])
            scenarios[current_scenario] = {'prob': scenario_prob, 'clients': {}}
        elif len(parts) == 4 and parts[0] == 'RHS':
            client = int(parts[1][1:]) - 7  # c7 corresponds to client 0
            availability = int(parts[3])
            scenarios[current_scenario]['clients'][client] = availability

    # Print some debug information
    print(f"Number of scenarios: {len(scenarios)}")
    if scenarios:
        first_scenario = next(iter(scenarios.values()))
        print(f"Number of clients in first scenario: {len(first_scenario['clients'])}")
        print(f"Sample of first scenario data: {list(first_scenario['clients'].items())[:5]}")

    return scenarios

def create_model(num_servers, num_clients, fixed_costs, revenues, capacity, scenarios):
    model = pyo.ConcreteModel()

    # Sets
    model.I = pyo.RangeSet(0, num_clients-1)  # Clients
    model.J = pyo.RangeSet(0, num_servers-1)  # Servers
    model.S = pyo.Set(initialize=scenarios.keys())  # Scenarios

    # First-stage variables
    model.x = pyo.Var(model.J, domain=pyo.Binary)

    # Second-stage variables
    model.y = pyo.Var(model.I, model.J, model.S, domain=pyo.Binary)

    # Objective function
    def obj_rule(model):
        first_stage = sum(fixed_costs[j] * model.x[j] for j in model.J)
        second_stage = sum(scenarios[s]['prob'] * sum(revenues.get((i,j), 0) * model.y[i,j,s] 
                           for i in model.I for j in model.J) for s in model.S)
        return first_stage - second_stage  # Minimize costs - revenues

    model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

    # Constraints
    def capacity_rule(model, j, s):
        return sum(model.y[i,j,s] for i in model.I) <= capacity * model.x[j]

    model.capacity = pyo.Constraint(model.J, model.S, rule=capacity_rule)

    def assignment_rule(model, i, s):
        return sum(model.y[i,j,s] for j in model.J) <= scenarios[s]['clients'].get(i, 0)

    model.assignment = pyo.Constraint(model.I, model.S, rule=assignment_rule)

    # Maximum number of servers
    model.max_servers = pyo.Constraint(expr=sum(model.x[j] for j in model.J) <= 5)

    return model

def solve_model(model):
    solver = pyopt.SolverFactory('glpk')
    results = solver.solve(model, tee=True)

    if results.solver.status == pyopt.SolverStatus.ok and results.solver.termination_condition == pyopt.TerminationCondition.optimal:
        print("Optimal solution found")
        print("Opened servers:")
        for j in model.J:
            if pyo.value(model.x[j]) > 0.5:
                print(f"Server {j+1}")
        
        print("\nObjective value:", pyo.value(model.obj))
    else:
        print("Solver did not find an optimal solution")

def main():
    cor_file_path = '/Users/vivekchaudhary/Documents/progressive_hedging/sslp/sslp_5_25_50.cor'
    sto_file_path = '/Users/vivekchaudhary/Documents/progressive_hedging/sslp/sslp_5_25_50.sto'

    num_servers, num_clients, fixed_costs, revenues, capacity = read_cor_file(cor_file_path)
    scenarios = read_sto_file(sto_file_path)

    model = create_model(num_servers, num_clients, fixed_costs, revenues, capacity, scenarios)
    solve_model(model)

if __name__ == "__main__":
    main()
 # cor_file_path = '/Users/vivekchaudhary/Documents/progressive_hedging/sslp/sslp_5_25_50.cor'
    # sto_file_path = '/Users/vivekchaudhary/Documents/progressive_hedging/sslp/sslp_5_25_50.sto'
