use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let lines = input.lines().collect::<Vec<_>>();
    let mut times = vec![];
    for x in lines[0].split_whitespace() {
        if let Ok(x) = x.parse::<i64>() {
            times.push(x);
        }
    }
    let mut distances = vec![];
    for x in lines[1].split_whitespace() {
        if let Ok(x) = x.parse::<i64>() {
            distances.push(x);
        }
    }

    let mut product_of_ways = 1;

    for race_index in 0..times.len() {
        let time = times[race_index];
        let distance = distances[race_index];
        let mut ways = 0;
        for time_held in 0..time {
            let speed = time_held;
            let distance_travelled = speed * (time - time_held);
            if distance_travelled > distance {
                ways += 1;
            }
        }
        product_of_ways *= ways;
    }
    println!("Part 1: {}", product_of_ways);
}

fn part2(input: &str) {
    let lines = input.lines().collect::<Vec<_>>();
    let times_str = lines[0].replace(" ", "");
    let time = times_str.split(":").nth(1).unwrap().parse::<i64>().unwrap();
    let distances_str = lines[1].replace(" ", "");
    let distance = distances_str
        .split(":")
        .nth(1)
        .unwrap()
        .parse::<i64>()
        .unwrap();

    let mut min_possible = -1;
    let mut max_possible = time;

    for time_held in 0..time {
        let speed = time_held;
        let distance_travelled = speed * (time - time_held);
        if distance_travelled > distance {
            min_possible = time_held;
            break;
        }
    }

    for time_held in (0..time).rev() {
        let speed = time_held;
        let distance_travelled = speed * (time - time_held);
        if distance_travelled > distance {
            max_possible = time_held;
            break;
        }
    }

    println!("Part 2: {}", (max_possible - min_possible) + 1);
}
