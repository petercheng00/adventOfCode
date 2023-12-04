use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut sum = 0;
    for line in input.lines() {
        let (_, all_nums) = line.split_once(":").unwrap();
        let (winners, numbers) = all_nums.split_once("|").unwrap();
        let winners: Vec<_> = winners.split_whitespace().collect();
        let numbers: Vec<_> = numbers.split_whitespace().collect();
        let winners: Vec<_> = winners.iter().map(|x| x.parse::<i32>().unwrap()).collect();
        let numbers: Vec<_> = numbers.iter().map(|x| x.parse::<i32>().unwrap()).collect();

        let mut num_matches = 0;
        for num in numbers {
            if winners.contains(&num) {
                num_matches += 1;
            }
        }

        if num_matches > 0 {
            sum += (2 as u32).pow((num_matches - 1) as u32);
        }
    }

    println!("Part 1: {}", sum);
}

fn part2(input: &str) {
    let mut card_winners = vec![];
    let mut card_nums = vec![];
    for line in input.lines() {
        let (_, all_nums) = line.split_once(":").unwrap();
        let (winners, numbers) = all_nums.split_once("|").unwrap();
        let winners: Vec<_> = winners.split_whitespace().collect();
        let numbers: Vec<_> = numbers.split_whitespace().collect();
        let winners: Vec<_> = winners.iter().map(|x| x.parse::<i32>().unwrap()).collect();
        let numbers: Vec<_> = numbers.iter().map(|x| x.parse::<i32>().unwrap()).collect();
        card_winners.push(winners);
        card_nums.push(numbers);
    }
    let mut card_counts = vec![1; card_winners.len()];
    for card_index in 0..card_winners.len() {
        let mut num_matches = 0;
        for num in &card_nums[card_index] {
            if card_winners[card_index].contains(&num) {
                num_matches += 1;
            }
        }
        for i in card_index + 1..=card_index + num_matches {
            if i < card_counts.len() {
                card_counts[i] += card_counts[card_index];
            }
        }
    }
    let sum_card_counts = card_counts.iter().sum::<i32>();
    println!("Part 2: {}", sum_card_counts);
}
