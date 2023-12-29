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
    for _step in 0..64 {
        let mut next_xys = HashSet::with_capacity(possible_xys.len() * DIRS.len());
        for start_xy in &possible_xys {
            for dir in &DIRS {
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

fn load_grid(input: &str) -> Array2<char> {
    let lines = input.lines().collect::<Vec<_>>();
    let shape = (lines.len(), lines[0].len());
    Array2::from_shape_fn(shape, |(i, j)| lines[i].chars().nth(j).unwrap())
}

fn get_modulo_grid(grid: &Array2<char>, xy: &Vec2) -> char {
    let x = xy.x.rem_euclid(grid.ncols() as i64);
    let y = xy.y.rem_euclid(grid.nrows() as i64);
    grid[(y as usize, x as usize)]
}

fn part2(input: &str) {
    let mut grid = load_grid(input);
    let mut start_xy = None;
    for ((row, col), c) in grid.indexed_iter_mut() {
        if *c == 'S' {
            *c = '.';
            start_xy = Some(Vec2::new(col as i64, row as i64));
            break;
        }
    }

    let mut current_xys = HashSet::new();
    current_xys.insert(start_xy.unwrap());
    let mut prev_xys = HashSet::new();

    let num_steps = 5000_u64;
    let mut odd_count = 0;
    let mut even_count = 1;

    for step in 0..num_steps {
        if (step - 65) % 131 == 0 {
            println!(
                "{}, {}, {}",
                step,
                (step - 65) / 131,
                if step % 2 == 0 { even_count } else { odd_count }
            );
        }
        let mut next_xys = HashSet::with_capacity(current_xys.len() * DIRS.len());
        for current_xy in &current_xys {
            for dir in &DIRS {
                let xy = current_xy + dir;

                if get_modulo_grid(&grid, &xy) == '.'
                    && !prev_xys.contains(&xy)
                    && !next_xys.contains(&xy)
                {
                    next_xys.insert(xy);
                    if step % 2 == 0 {
                        odd_count += 1;
                    } else {
                        even_count += 1;
                    }
                }
            }
        }
        prev_xys = std::mem::replace(&mut current_xys, next_xys);
    }
}
