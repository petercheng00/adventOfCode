use std::collections::HashSet;

use ndarray::Array2;

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut grid = load_grid(input);
    let mut start_xy = None;
    for ((row, col), c) in grid.indexed_iter_mut() {
        if *c == 'S' {
            *c = '.';
            start_xy = Some(Vec2::new(col as i64, row as i64));
            break;
        }
    }
    let start_xy = start_xy.unwrap();
    let mut possible_xys = HashSet::new();
    possible_xys.insert(start_xy);
    let dirs = [LEFT, RIGHT, UP, DOWN];
    for _step in 0..64 {
        let mut next_xys = HashSet::with_capacity(possible_xys.len() * dirs.len());
        for start_xy in &possible_xys {
            for dir in &dirs {
                let xy = start_xy + dir;
                if xy.x < 0
                    || xy.y < 0
                    || xy.x >= grid.ncols() as i64
                    || xy.y >= grid.nrows() as i64
                {
                    continue;
                }
                let c = grid[(xy.y as usize, xy.x as usize)];
                if c == '.' {
                    next_xys.insert(xy);
                }
            }
        }
        possible_xys = next_xys;
    }
    println!("Part 1: {}", possible_xys.len());
}

fn part2(input: &str) {}

fn load_grid(input: &str) -> Array2<char> {
    let lines = input.lines().collect::<Vec<_>>();
    let shape = (lines.len(), lines[0].len());
    Array2::from_shape_fn(shape, |(i, j)| lines[i].chars().nth(j).unwrap())
}
