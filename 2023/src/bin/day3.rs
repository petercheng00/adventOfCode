use std::collections::HashMap;

use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let grid = input
        .lines()
        .map(|l| l.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let height = grid.len();
    let width = grid[0].len();

    let mut row = 0;
    let mut col = 0;
    let mut sum = 0;
    while row < height {
        while col < width {
            let c = grid[row][col];
            if !c.is_ascii_digit() {
                col += 1;
                continue;
            }
            // Get the start and end col for this number.
            let mut end_col = col;
            while end_col < width && grid[row][end_col].is_ascii_digit() {
                end_col += 1;
            }
            let first_col = col;
            let last_col = end_col - 1;

            if has_adjacent_symbol(&grid, row, first_col, last_col) {
                sum += parse_number(&grid, row, first_col, last_col);
            }
            col = end_col;
        }
        row += 1;
        col = 0;
    }

    println!("{}", sum);
}

fn is_symbol(c: char) -> bool {
    !c.is_ascii_digit() && c != '.'
}

fn has_adjacent_symbol(
    grid: &Vec<Vec<char>>,
    row: usize,
    first_col: usize,
    last_col: usize,
) -> bool {
    let row: i32 = row as i32;
    let first_col: i32 = first_col as i32;
    let last_col: i32 = last_col as i32;
    for row in row - 1..=row + 1 {
        if row < 0 || row >= grid.len() as i32 {
            continue;
        }
        for col in first_col - 1..=last_col + 1 {
            if col > 0 && col < grid[0].len() as i32 {
                if is_symbol(grid[row as usize][col as usize]) {
                    return true;
                }
            }
        }
    }
    false
}

fn parse_number(grid: &Vec<Vec<char>>, row: usize, first_col: usize, last_col: usize) -> u32 {
    let mut num = 0;
    for c in first_col..=last_col {
        num = num * 10 + grid[row][c].to_digit(10).unwrap();
    }
    num
}

fn part2(input: &str) {
    // Try to reuse above code. Create a map of gear xy -> Vec<number>
    let grid = input
        .lines()
        .map(|l| l.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let height = grid.len();
    let width = grid[0].len();

    let mut row = 0;
    let mut col = 0;
    let mut gear_xy_to_nums = HashMap::<(usize, usize), Vec<u32>>::new();
    while row < height {
        while col < width {
            let c = grid[row][col];
            if !c.is_ascii_digit() {
                col += 1;
                continue;
            }
            // Get the start and end col for this number.
            let mut end_col = col;
            while end_col < width && grid[row][end_col].is_ascii_digit() {
                end_col += 1;
            }
            let first_col = col;
            let last_col = end_col - 1;

            let num = parse_number(&grid, row, first_col, last_col);

            for gear_xy in get_adjacent_gears(&grid, row, first_col, last_col) {
                gear_xy_to_nums.entry(gear_xy).or_default().push(num);
            }

            col = end_col;
        }
        row += 1;
        col = 0;
    }

    let mut sum_gear_ratios = 0;
    for (_gear, nums) in gear_xy_to_nums {
        if nums.len() == 2 {
            sum_gear_ratios += nums[0] * nums[1];
        }
    }

    println!("{}", sum_gear_ratios);
}

fn get_adjacent_gears(
    grid: &Vec<Vec<char>>,
    row: usize,
    first_col: usize,
    last_col: usize,
) -> Vec<(usize, usize)> {
    let row: i32 = row as i32;
    let first_col: i32 = first_col as i32;
    let last_col: i32 = last_col as i32;
    let mut gear_xys = vec![];
    for row in row - 1..=row + 1 {
        if row < 0 || row >= grid.len() as i32 {
            continue;
        }
        for col in first_col - 1..=last_col + 1 {
            if col > 0 && col < grid[0].len() as i32 {
                if grid[row as usize][col as usize] == '*' {
                    gear_xys.push((col as usize, row as usize));
                }
            }
        }
    }
    gear_xys
}
