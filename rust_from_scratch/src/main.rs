mod bac;
use ndarray::{array, Array1, Array2};

fn main() {
    // Define the problem:
    // Maximize: 3x + 2y
    // Subject to:
    //    2x + y <= 8
    //    x + 3y <= 8
    //    x, y >= 0

    // Objective coefficients (note: we'll negate these in solve_lp)
    let c = array![3.0, 2.0];

    // Inequality constraints
    let a_ub = array![[2.0, 1.0], [1.0, 3.0]];
    let b_ub = array![8.0, 8.0];

    // No equality constraints for this problem
    let a_eq: Option<Array2<f64>> = None;
    let b_eq: Option<Array1<f64>> = None;

    // Bounds for variables (x >= 0, y >= 0)
    let bounds = vec![(Some(0.0), None), (Some(0.0), None)];

    match bac::solve_lp(&c, &a_ub, &b_ub, &a_eq, &b_eq, &bounds) {
        Some(solution) => {
            println!("Optimal solution found:");
            println!("x = {:.6}", solution[0]);
            println!("y = {:.6}", solution[1]);
            println!("Optimal value = {:.6}", c.dot(&solution));
        },
        None => println!("No solution found"),
    }
}