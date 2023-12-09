use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut sum_preds = 0;
    for line in input.lines() {
        let nums = line
            .split_whitespace()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<_>>();
        let mut all_nums = vec![nums];
        // Get differences until all zero.
        while all_nums.last().unwrap().iter().any(|x| *x != 0) {
            let differences = all_nums
                .last()
                .unwrap()
                .windows(2)
                .map(|x| x[1] - x[0])
                .collect::<Vec<_>>();
            all_nums.push(differences);
        }

        // Now go back up.
        let mut last_value = 0;
        for nums in all_nums.iter().rev() {
            last_value += nums.last().unwrap();
        }
        sum_preds += last_value;
    }
    println!("Part 1: {}", sum_preds);
}

fn part2(input: &str) {
    let mut sum_preds = 0;
    for line in input.lines() {
        let nums = line
            .split_whitespace()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<_>>();
        let mut all_nums = vec![nums];
        // Get differences until all zero.
        while all_nums.last().unwrap().iter().any(|x| *x != 0) {
            let differences = all_nums
                .last()
                .unwrap()
                .windows(2)
                .map(|x| x[1] - x[0])
                .collect::<Vec<_>>();
            all_nums.push(differences);
        }

        // Now go back up.
        let mut before_value = 0;
        for nums in all_nums.iter().rev() {
            before_value = nums.first().unwrap() - before_value;
        }
        sum_preds += before_value;
    }
    println!("Part 2: {}", sum_preds);
}
