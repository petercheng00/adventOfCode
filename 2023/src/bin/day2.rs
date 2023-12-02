use std::collections::HashMap;

use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let actual_counts = HashMap::from([("red", 12), ("green", 13), ("blue", 14)]);
    let mut sum_valid_ids = 0;
    'line_loop: for line in input.lines() {
        let (game_id, sets) = line.split_once(":").unwrap();
        let game_id = game_id
            .strip_prefix("Game ")
            .unwrap()
            .parse::<usize>()
            .unwrap();
        for set in sets.split(";") {
            for cubes in set.split(",") {
                let (count, color) = cubes.trim().split_once(" ").unwrap();
                let count = count.parse::<usize>().unwrap();
                if *actual_counts.get(color).unwrap() < count {
                    continue 'line_loop;
                }
            }
        }
        sum_valid_ids += game_id;
    }
    println!("Part 1: {}", sum_valid_ids);
}

fn part2(input: &str) {
    let mut sum_powers = 0;
    for line in input.lines() {
        let (_game_id, sets) = line.split_once(":").unwrap();
        let mut min_possible_counts = HashMap::from([("red", 0), ("green", 0), ("blue", 0)]);
        for set in sets.split(";") {
            for cubes in set.split(",") {
                let (count, color) = cubes.trim().split_once(" ").unwrap();
                let count = count.parse::<i32>().unwrap();
                min_possible_counts
                    .entry(color)
                    .and_modify(|c| *c = (*c).max(count));
            }
        }
        sum_powers += min_possible_counts.values().product::<i32>();
    }
    println!("Part 2: {}", sum_powers);
}
