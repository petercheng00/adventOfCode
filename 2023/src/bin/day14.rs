use std::collections::HashMap;

use ndarray::Array2;

use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut grid = load_grid(input);
    tilt_north(&mut grid);
    println!("Part 1: {}", north_load(&grid));
}

fn part2(input: &str) {
    let mut grid = load_grid(input);
    let (repeat_start, repeat_len) = find_repeat(&mut grid);
    let num_cycles_left = (1000000000 - repeat_start) % repeat_len;
    for _ in 0..num_cycles_left {
        spin_cycle(&mut grid);
    }
    println!("Part 2: {}", north_load(&grid));
}

fn load_grid(input: &str) -> Array2<char> {
    let lines = input.lines().collect::<Vec<_>>();
    let shape = (lines.len(), lines[0].len());
    Array2::from_shape_fn(shape, |(i, j)| lines[i].chars().nth(j).unwrap())
}

fn tilt_north(grid: &mut Array2<char>) {
    for row in 0..grid.shape()[0] {
        for col in 0..grid.shape()[1] {
            if grid[[row, col]] != 'O' {
                continue;
            }
            grid[[row, col]] = '.';
            let mut new_row = row as isize;
            while new_row - 1 >= 0 && grid[[(new_row - 1) as usize, col]] == '.' {
                new_row -= 1;
            }
            grid[[new_row as usize, col]] = 'O';
        }
    }
}

fn north_load(grid: &Array2<char>) -> usize {
    let mut sum_load = 0;
    for ((row, _col), val) in grid.indexed_iter() {
        if *val == 'O' {
            sum_load += grid.shape()[0] - row;
        }
    }
    sum_load
}

fn rot90cw(grid: &mut Array2<char>) {
    let mut new_grid = grid.clone();
    for ((row, col), val) in grid.indexed_iter() {
        new_grid[[col, grid.shape()[1] - 1 - row]] = *val;
    }
    *grid = new_grid;
}

fn spin_cycle(grid: &mut Array2<char>) {
    tilt_north(grid);
    rot90cw(grid);
    tilt_north(grid);
    rot90cw(grid);
    tilt_north(grid);
    rot90cw(grid);
    tilt_north(grid);
    rot90cw(grid);
}

// Find a repeat, and return the start and length of the repeat.
fn find_repeat(grid: &mut Array2<char>) -> (i32, i32) {
    let mut grids_to_cycles: HashMap<Array2<char>, Vec<i32>> = std::collections::HashMap::new();
    for cycle in 0..1000000000 {
        spin_cycle(grid);
        let entry = grids_to_cycles.entry(grid.clone()).or_default();
        entry.push(cycle + 1);
        if entry.len() == 3 {
            // 3 is good enough for a pattern right?
            if entry[2] - entry[1] == entry[1] - entry[0] {
                return (entry[0], entry[1] - entry[0]);
            }
        }
    }
    panic!("Failed!");
}
