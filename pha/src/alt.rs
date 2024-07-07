// pub mod pha;

// use ndarray::{Array1, Array2};
// use good_lp::{variables, variable, constraint, SolverModel, Solution, ProblemVariables};
// use good_lp::default_solver;  // Add this import

// struct MIPProblem {
//     c: Array1<f64>,
//     a_ub: Array2<f64>,
//     b_ub: Array1<f64>,
//     a_eq: Option<Array2<f64>>,
//     b_eq: Option<Array1<f64>>,
//     bounds: Vec<(Option<f64>, Option<f64>)>,
//     int_vars: Vec<usize>,
// }

// struct Node {
//     bounds: Vec<(Option<f64>, Option<f64>)>,
//     solution: Option<Array1<f64>>,
//     objective: Option<f64>,
// }




// fn solve_lp(c: &Array1<f64>, a_ub: &Array2<f64>, b_ub: &Array1<f64>, a_eq: &Option<Array2<f64>>, b_eq: &Option<Array1<f64>>, bounds: &Vec<(Option<f64>, Option<f64>)>) -> Option<Array1<f64>> {
//     let mut vars = variables!();
//     let num_vars = c.len();

//     // Create variables with bounds
//     let x: Vec<_> = (0..num_vars)
//         .map(|i| {
//             let (lb, ub) = bounds[i];
//             let mut var = variable().min(lb.unwrap_or(f64::NEG_INFINITY));
//             if let Some(upper) = ub {
//                 var = var.max(upper);
//             }
//             vars.add(var)
//         })
//         .collect();

//     // Set up the objective function
//     let objective = c.iter().zip(x.iter()).map(|(&c_i, &x_i)| c_i * x_i).sum();

//     // Create the problem, starting with the objective
//     let mut problem = vars.minimise(objective);

//     // Add inequality constraints
//     for (row, &b) in a_ub.outer_iter().zip(b_ub.iter()) {
//         let lhs = row.iter().zip(x.iter()).map(|(&a, &x)| a * x).sum();
//         problem = problem.add_constraint(lhs.leq(b));
//     }

//     // Add equality constraints if they exist
//     if let (Some(a_eq), Some(b_eq)) = (a_eq, b_eq) {
//         for (row, &b) in a_eq.outer_iter().zip(b_eq.iter()) {
//             let lhs = row.iter().zip(x.iter()).map(|(&a, &x)| a * x).sum();
//             problem = problem.add_constraint(lhs.eq(b));
//         }
//     }

//     // Solve the problem
//     match problem.using(default_solver).solve() {
//         Ok(solution) => {
//             let result = Array1::from_iter(x.iter().map(|&v| solution.value(v)));
//             Some(result)
//         },
//         Err(_) => None,
//     }
// }


// fn is_integer(x: &Array1<f64>, tol: f64) -> bool {
//     x.iter().all(|&val| (val - val.round()).abs() < tol)
// }

// fn generate_cut(x: &Array1<f64>, a: &Array2<f64>, b: &Array1<f64>) -> (Array1<f64>, f64) {
//     let row = x.iter().enumerate()
//         .max_by(|&(_, a), &(_, b)| (a - a.round()).abs().partial_cmp(&(b - b.round()).abs()).unwrap())
//         .map(|(index, _)| index)
//         .unwrap();
    
//     let f = x[row] - x[row].floor();
//     let mut cut = a.row(row).to_owned().mapv(|x| x.floor()) - a.row(row).to_owned();
//     cut.mapv_inplace(|x| if x < 0.0 { 0.0 } else { x });
//     let rhs = b[row].floor() - f;
    
//     (cut, rhs)
// }

// fn branch_and_cut(problem: &MIPProblem, node: &Node) -> Option<(Array1<f64>, f64)> {
//     let bounds = node.bounds.iter().enumerate().map(|(i, &(lb, ub))| {
//         (
//             match (lb, problem.bounds[i].0) {
//                 (Some(a), Some(b)) => Some(a.max(b)),
//                 (Some(a), None) => Some(a),
//                 (None, Some(b)) => Some(b),
//                 (None, None) => None,
//             },
//             match (ub, problem.bounds[i].1) {
//                 (Some(a), Some(b)) => Some(a.min(b)),
//                 (Some(a), None) => Some(a),
//                 (None, Some(b)) => Some(b),
//                 (None, None) => None,
//             },
//         )
//     }).collect::<Vec<_>>();

//     let x = solve_lp(&problem.c, &problem.a_ub, &problem.b_ub, &problem.a_eq, &problem.b_eq, &bounds)?;
    
//     let obj = problem.c.dot(&x);
    
//     if is_integer(&x.select(ndarray::Axis(0), &problem.int_vars), 1e-6) {
//         return Some((x, obj));
//     }
    
//     let (cut, rhs) = generate_cut(&x, &problem.a_ub, &problem.b_ub);
//     let mut new_a_ub = ndarray::stack(ndarray::Axis(0), &[problem.a_ub.view(), cut.view().into_shape((1, cut.len())).unwrap()]).unwrap();
//     let mut new_b_ub = ndarray::stack(ndarray::Axis(0), &[problem.b_ub.view(), ndarray::arr1(&[rhs]).view()]).unwrap();
    
//     let x = solve_lp(&problem.c, &new_a_ub, &new_b_ub, &problem.a_eq, &problem.b_eq, &bounds)?;
    
//     if is_integer(&x.select(ndarray::Axis(0), &problem.int_vars), 1e-6) {
//         return Some((x, problem.c.dot(&x)));
//     }
    
//     let var = problem.int_vars[x.select(ndarray::Axis(0), &problem.int_vars)
//         .iter()
//         .enumerate()
//         .max_by(|&(_, a), &(_, b)| (a - a.round()).abs().partial_cmp(&(b - b.round()).abs()).unwrap())
//         .map(|(index, _)| index)
//         .unwrap()];
    
//     let mut left_bounds = bounds.clone();
//     left_bounds[var].1 = Some(x[var].floor());
//     let left_node = Node { bounds: left_bounds, solution: None, objective: None };
//     let left_result = branch_and_cut(problem, &left_node);
    
//     let mut right_bounds = bounds;
//     right_bounds[var].0 = Some(x[var].ceil());
//     let right_node = Node { bounds: right_bounds, solution: None, objective: None };
//     let right_result = branch_and_cut(problem, &right_node);
    
//     match (left_result, right_result) {
//         (Some((x_left, obj_left)), Some((x_right, obj_right))) => {
//             if obj_left > obj_right {
//                 Some((x_left, obj_left))
//             } else {
//                 Some((x_right, obj_right))
//             }
//         },
//         (Some(left), None) => Some(left),
//         (None, Some(right)) => Some(right),
//         (None, None) => None,
//     }
// }

// fn solve_mip(c: Array1<f64>, a_ub: Array2<f64>, b_ub: Array1<f64>, a_eq: Option<Array2<f64>>, b_eq: Option<Array1<f64>>, 
//              bounds: Vec<(Option<f64>, Option<f64>)>, int_vars: Vec<usize>, minimize: bool) -> Option<(Array1<f64>, f64)> {
//     let c = if minimize { c } else { -c };
    
//     let problem = MIPProblem { c, a_ub, b_ub, a_eq, b_eq, bounds: bounds.clone(), int_vars };
//     let root = Node { bounds, solution: None, objective: None };
    
//     let (x, obj) = branch_and_cut(&problem, &root)?;
    
//     Some((x, if minimize { obj } else { -obj }))
// }

// fn main() {
//     // Example usage would go here
// }