use aoc2020_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &String) {
    let nums: Vec<i32> = input
        .lines()
        .map(|line| line.parse().expect("Input lines should all be integers."))
        .collect();
    for (i, x) in nums.iter().enumerate() {
        for y in &nums[i + 1..] {
            if x + y == 2020 {
                println!("{}", x * y);
                return;
            }
        }
    }
    println!("Failed to find a solution.");
}

fn part2(input: &String) {
    let nums: Vec<i32> = input
        .lines()
        .map(|line| line.parse().expect("Input lines should all be integers."))
        .collect();
    for (i, x) in nums.iter().enumerate() {
        for (j, y) in nums[i + 1..].iter().enumerate() {
            for z in &nums[j + 1..] {
                if x + y + z == 2020 {
                    println!("{}", x * y * z);
                    return;
                }
            }
        }
    }
    println!("Failed to find a solution.");
}
