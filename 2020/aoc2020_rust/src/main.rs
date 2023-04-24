use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    let input_filename = args.get(1);

    if let Some(filename) = input_filename {
        let input_str =
            fs::read_to_string(filename).expect("Should have been able to read the file");
        day1_1(&input_str);
        day1_2(&input_str);
    } else {
        println!("Provide an input filename.");
    }
}

fn day1_1(input: &String) {
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

fn day1_2(input: &String) {
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
