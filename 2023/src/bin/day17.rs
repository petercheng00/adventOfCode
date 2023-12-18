use std::collections::{BinaryHeap, HashMap};

use ndarray::Array2;

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let grid = load_grid(input);
    println!("Part 1: {}", min_heat_loss(grid));
}

fn part2(input: &str) {
    let grid = load_grid(input);
    println!("Part 2: {}", min_heat_loss2(grid));
}

fn load_grid(input: &str) -> Array2<u8> {
    let lines = input.lines().collect::<Vec<_>>();
    let shape = (lines.len(), lines[0].len());
    Array2::from_shape_fn(shape, |(i, j)| {
        lines[i].chars().nth(j).unwrap().to_digit(10).unwrap() as u8
    })
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct State {
    moves: MoveHistory,
    cost_so_far: u32,
    dst: Vec2,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct MoveHistory {
    xy: Vec2,
    recent_move_dirs: Vec<Vec2>,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let astar_cost = self.cost_so_far as i32 + (self.dst - self.moves.xy).abs().sum();
        let astar_cost_other = other.cost_so_far as i32 + (other.dst - other.moves.xy).abs().sum();
        astar_cost_other.cmp(&astar_cost)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.cmp(other).into()
    }
}

fn min_heat_loss(grid: Array2<u8>) -> u32 {
    let start_state = State {
        moves: MoveHistory {
            xy: Vec2::new(0, 0),
            recent_move_dirs: vec![],
        },
        cost_so_far: 0,
        dst: Vec2::new(grid.shape()[1] as i32 - 1, grid.shape()[0] as i32 - 1),
    };

    let mut pq = BinaryHeap::new();
    pq.push(start_state);

    let mut state_to_min_cost = HashMap::new();

    while let Some(state) = pq.pop() {
        if state.moves.xy == Vec2::new(grid.shape()[1] as i32 - 1, grid.shape()[0] as i32 - 1) {
            // Done.
            return state.cost_so_far;
        }
        for state in evolve_state(&grid, &state) {
            if state.cost_so_far < *state_to_min_cost.get(&state.moves).unwrap_or(&u32::MAX) {
                state_to_min_cost.insert(state.moves.clone(), state.cost_so_far);
                pq.push(state);
            }
        }
    }

    panic!("Failed!");
}

fn evolve_state(grid: &Array2<u8>, state: &State) -> Vec<State> {
    let mut next_states = vec![];

    let prev_direction = *state
        .moves
        .recent_move_dirs
        .last()
        .unwrap_or(&Vec2::new(0, 0));
    let three_in_a_row = state.moves.recent_move_dirs.len() >= 3
        && state.moves.recent_move_dirs[state.moves.recent_move_dirs.len() - 3..]
            .iter()
            .all(|&dir| dir == prev_direction);

    for &dir in &[LEFT, RIGHT, UP, DOWN] {
        // Can't go opposite from prev_direction.
        if dir == -prev_direction {
            continue;
        }
        // Can't continue in same direction if 3 in a row.
        if dir == prev_direction && three_in_a_row {
            continue;
        }
        let new_xy = state.moves.xy + dir;
        // Can't go out of bounds.
        if new_xy.x < 0
            || new_xy.y < 0
            || new_xy.x >= grid.shape()[1] as i32
            || new_xy.y >= grid.shape()[0] as i32
        {
            continue;
        }

        let new_cost = state.cost_so_far + grid[[new_xy.y as usize, new_xy.x as usize]] as u32;
        let mut new_recent_move_dirs = state.moves.recent_move_dirs.clone();
        new_recent_move_dirs.push(dir);
        if new_recent_move_dirs.len() > 3 {
            new_recent_move_dirs.remove(0);
        }
        next_states.push(State {
            moves: MoveHistory {
                xy: new_xy,
                recent_move_dirs: new_recent_move_dirs,
            },
            cost_so_far: new_cost,
            dst: state.dst,
        });
    }

    next_states
}

fn min_heat_loss2(grid: Array2<u8>) -> u32 {
    let start_state = State {
        moves: MoveHistory {
            xy: Vec2::new(0, 0),
            recent_move_dirs: vec![],
        },
        cost_so_far: 0,
        dst: Vec2::new(grid.shape()[1] as i32 - 1, grid.shape()[0] as i32 - 1),
    };

    let mut pq = BinaryHeap::new();
    pq.push(start_state);

    let mut state_to_min_cost = HashMap::new();

    while let Some(state) = pq.pop() {
        if state.moves.xy == Vec2::new(grid.shape()[1] as i32 - 1, grid.shape()[0] as i32 - 1) {
            // Done.
            return state.cost_so_far;
        }
        for state in evolve_state2(&grid, &state) {
            if state.cost_so_far < *state_to_min_cost.get(&state.moves).unwrap_or(&u32::MAX) {
                state_to_min_cost.insert(state.moves.clone(), state.cost_so_far);
                pq.push(state);
            }
        }
    }

    panic!("Failed!");
}

fn evolve_state2(grid: &Array2<u8>, state: &State) -> Vec<State> {
    let mut next_states = vec![];

    let prev_direction = *state
        .moves
        .recent_move_dirs
        .last()
        .unwrap_or(&Vec2::new(0, 0));
    let ten_in_a_row = state.moves.recent_move_dirs.len() >= 10
        && state.moves.recent_move_dirs[state.moves.recent_move_dirs.len() - 10..]
            .iter()
            .all(|&dir| dir == prev_direction);

    for &dir in &[LEFT, RIGHT, UP, DOWN] {
        // Can't go opposite from prev_direction.
        if dir == -prev_direction {
            continue;
        }
        // Can't continue in same direction if 3 in a row.
        if dir == prev_direction && ten_in_a_row {
            continue;
        }
        // If new direction, go 4 steps since that's required.
        let step_amount = if dir != prev_direction { 4 } else { 1 };
        let new_xy = state.moves.xy + step_amount * dir;
        // Can't go out of bounds.
        if new_xy.x < 0
            || new_xy.y < 0
            || new_xy.x >= grid.shape()[1] as i32
            || new_xy.y >= grid.shape()[0] as i32
        {
            continue;
        }

        let mut new_cost = state.cost_so_far;
        let mut new_recent_move_dirs = state.moves.recent_move_dirs.clone();
        for step in 1..=step_amount {
            let xy = state.moves.xy + step * dir;
            new_cost += grid[[xy.y as usize, xy.x as usize]] as u32;
            new_recent_move_dirs.push(dir);
        }
        while new_recent_move_dirs.len() > 10 {
            new_recent_move_dirs.remove(0);
        }

        next_states.push(State {
            moves: MoveHistory {
                xy: new_xy,
                recent_move_dirs: new_recent_move_dirs,
            },
            cost_so_far: new_cost,
            dst: state.dst,
        });
    }

    next_states
}
