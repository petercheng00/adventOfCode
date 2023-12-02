use std::collections::HashMap;

use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut sum = 0;
    for line in input.lines() {
        let first_digit = line
            .chars()
            .find(|c| c.is_ascii_digit())
            .unwrap()
            .to_digit(10)
            .unwrap();
        let last_digit = line
            .chars()
            .rev()
            .find(|c| c.is_ascii_digit())
            .unwrap()
            .to_digit(10)
            .unwrap();
        sum += first_digit * 10 + last_digit;
    }
    println!("Part 1: {}", sum);
}

fn part2(input: &str) {
    let digits = HashMap::from([
        ("1".to_owned(), 1),
        ("2".to_owned(), 2),
        ("3".to_owned(), 3),
        ("4".to_owned(), 4),
        ("5".to_owned(), 5),
        ("6".to_owned(), 6),
        ("7".to_owned(), 7),
        ("8".to_owned(), 8),
        ("9".to_owned(), 9),
        ("one".to_owned(), 1),
        ("two".to_owned(), 2),
        ("three".to_owned(), 3),
        ("four".to_owned(), 4),
        ("five".to_owned(), 5),
        ("six".to_owned(), 6),
        ("seven".to_owned(), 7),
        ("eight".to_owned(), 8),
        ("nine".to_owned(), 9),
    ]);
    let reverse_digits = digits
        .iter()
        .map(|(k, &v)| (k.chars().rev().collect::<String>(), v))
        .collect::<HashMap<_, _>>();

    let mut sum = 0;
    for line in input.lines() {
        let first_digit = find_digit(line, &digits);
        let last_digit = find_digit(&line.chars().rev().collect::<String>(), &reverse_digits);
        sum += first_digit * 10 + last_digit;
    }
    println!("Part 2: {}", sum);
}

fn find_digit(line: &str, digits_map: &HashMap<String, u32>) -> u32 {
    for i in 0..line.len() {
        for (digit_str, value) in digits_map {
            if line[i..].starts_with(digit_str) {
                return *value;
            }
        }
    }
    panic!("No digit found in line: {}", line);
}
