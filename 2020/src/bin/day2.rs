use aoc2020_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn parse_line(line: &str) -> (usize, usize, char, &str) {
    let mut line_parts = line.split_whitespace();
    let mut range = line_parts.next().unwrap().split("-");
    let num1: usize = range.next().unwrap().parse().unwrap();
    let num2: usize = range.next().unwrap().parse().unwrap();
    let character = line_parts.next().unwrap().chars().next().unwrap();
    let password = line_parts.next().unwrap();

    (num1, num2, character, password)
}

fn part1(input: &String) {
    let mut num_good_passwords = 0;
    for line in input.lines() {
        let (range_min, range_max, character, password) = parse_line(line);

        let char_count = password.matches(character).count();
        if char_count >= range_min && char_count <= range_max {
            num_good_passwords += 1;
        }
    }
    println!("{num_good_passwords}");
}

fn part2(input: &String) {
    let mut num_good_passwords = 0;
    for line in input.lines() {
        let (index1, index2, character, password) = parse_line(line);

        let match1 = character == password.chars().nth(index1 - 1).unwrap();
        let match2 = character == password.chars().nth(index2 - 1).unwrap();

        if match1 ^ match2 {
            num_good_passwords += 1;
        }
    }
    println!("{num_good_passwords}");
}
