use good_lp::{Variable, variables, variable, Expression, LpProblem, Solution, SolverModel};
use good_lp::solvers::highs;
use ndarray::{Array1, Array2};

pub fn solve_lp(
    c: &Array1<f64>,
    a_ub: &Array2<f64>,
    b_ub: &Array1<f64>,
    a_eq: &Option<Array2<f64>>,
    b_eq: &Option<Array1<f64>>,
    bounds: &Vec<(Option<f64>, Option<f64>)>
) -> Option<Array1<f64>> {
    let mut vars = variables!();
    let num_vars = c.len();

    // Create variables with bounds
    let x: Vec<Variable> = (0..num_vars)
        .map(|i| {
            let (lb, ub) = bounds[i];
            let mut var = variable();
            if let Some(lower) = lb {
                var = var.min(lower);
            }
            if let Some(upper) = ub {
                var = var.max(upper);
            }
            vars.add(var)
        })
        .collect();

    // Set up the objective function (note the negation for maximization)
    let objective: Expression = c.iter().zip(x.iter()).map(|(&c_i, &x_i)| -c_i * x_i).sum();

    // Create the problem, starting with the objective
    let mut problem = vars.minimise(objective).using(highs);

    // Add inequality constraints
    for (row, &b) in a_ub.outer_iter().zip(b_ub.iter()) {
        let lhs: Expression = row.iter().zip(x.iter()).map(|(&a, &x)| a * x).sum();
        problem = problem.add_constraint(lhs.le(b));
    }

    // Add equality constraints if they exist
    if let (Some(a_eq), Some(b_eq)) = (a_eq, b_eq) {
        for (row, &b) in a_eq.outer_iter().zip(b_eq.iter()) {
            let lhs: Expression = row.iter().zip(x.iter()).map(|(&a, &x)| a * x).sum();
            problem = problem.add_constraint(lhs.eq(b));
        }
    }

    // Solve the problem
    match problem.solve() {
        Ok(solution) => {
            let result = Array1::from_iter(x.iter().map(|&v| solution.value(v)));
            Some(result)
        },
        Err(_) => None,
    }
}