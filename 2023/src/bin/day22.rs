use std::collections::VecDeque;

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut bricks = load_bricks(input);
    do_gravity(&mut bricks);
    println!("Part 1: {}", num_can_be_disintegrated(&bricks));
}

fn part2(input: &str) {
    let mut bricks = load_bricks(input);
    do_gravity(&mut bricks);
    let mut supports = vec![vec![]; bricks.len()];
    let mut on_top_ofs = vec![vec![]; bricks.len()];
    for i in 0..bricks.len() {
        for j in 0..bricks.len() {
            if i == j {
                continue;
            }
            if on_top_of(&bricks[j], &bricks[i]) {
                supports[i].push(j);
                on_top_ofs[j].push(i);
            }
        }
    }
    let mut total_count = 0;
    for i in 0..bricks.len() {
        // Try disintegrating i.
        let mut fallen = vec![i];
        let mut queue = VecDeque::new();
        for &j in &supports[i] {
            queue.push_back(j);
        }
        while let Some(j) = queue.pop_front() {
            if fallen.contains(&j) {
                continue;
            }
            // See if j falls now.
            // j falls if everything its on top of has fallen
            let mut falls = true;
            for &k in &on_top_ofs[j] {
                if !fallen.contains(&k) {
                    falls = false;
                    break;
                }
            }
            // if j falls, add it to fallen and add its supports elements to the queue.
            if falls {
                fallen.push(j);
                for &k in &supports[j] {
                    queue.push_back(k);
                }
            }
        }
        // Don't include the brick we disintegrated.
        let count = fallen.len() - 1;
        total_count += count;
    }
    println!("Part 2: {}", total_count);
}

#[derive(Clone, Debug, PartialEq)]
struct Brick {
    min: Vec3,
    max: Vec3,
}

fn load_bricks(input: &str) -> Vec<Brick> {
    // Each line is a brick, x1,y1,z1~x2,y2,z2
    input
        .lines()
        .map(|line| {
            let (p1, p2) = line.split_once('~').unwrap();
            let p1 = p1
                .split(',')
                .map(|s| s.parse::<i64>().unwrap())
                .collect::<Vec<_>>();
            let p2 = p2
                .split(',')
                .map(|s| s.parse::<i64>().unwrap())
                .collect::<Vec<_>>();
            let p1 = Vec3::new(p1[0], p1[1], p1[2]);
            let p2 = Vec3::new(p2[0], p2[1], p2[2]);

            Brick {
                min: Vec3::new(p1.x.min(p2.x), p1.y.min(p2.y), p1.z.min(p2.z)),
                max: Vec3::new(p1.x.max(p2.x), p1.y.max(p2.y), p1.z.max(p2.z)),
            }
        })
        .collect()
}

fn on_ground(a: &Brick) -> bool {
    a.min.z == 1
}

fn on_top_of(a: &Brick, b: &Brick) -> bool {
    if a.min.z != b.max.z + 1 {
        return false;
    }
    if a.min.x > b.max.x || a.max.x < b.min.x {
        return false;
    }
    if a.min.y > b.max.y || a.max.y < b.min.y {
        return false;
    }
    true
}

fn do_gravity(bricks: &mut [Brick]) {
    loop {
        let mut something_happened = false;
        for i in 0..bricks.len() {
            if bricks[i].min.z <= 0 {
                // hack. we hide bricks underground sometimes.
                continue;
            }
            if on_ground(&bricks[i]) {
                continue;
            }
            let mut on_top_of_something = false;
            for j in 0..bricks.len() {
                if i == j {
                    continue;
                }
                if on_top_of(&bricks[i], &bricks[j]) {
                    on_top_of_something = true;
                    break;
                }
            }
            if !on_top_of_something {
                bricks[i].min.z -= 1;
                bricks[i].max.z -= 1;
                something_happened = true;
            }
        }

        if !something_happened {
            break;
        }
    }
}

fn num_can_be_disintegrated(bricks: &[Brick]) -> i32 {
    // can be disintegrated if every brick on top of me is supported by at least 2 bricks.
    let mut num_on_top_of = vec![];
    for i in 0..bricks.len() {
        num_on_top_of.push(0);
        for j in 0..bricks.len() {
            if i == j {
                continue;
            }
            if on_top_of(&bricks[i], &bricks[j]) {
                num_on_top_of[i] += 1;
            }
        }
    }

    let mut num_can_be_disintegrated = 0;
    for i in 0..bricks.len() {
        let mut safe_to_disintegrate = true;
        for j in 0..bricks.len() {
            if i == j {
                continue;
            }
            if on_top_of(&bricks[j], &bricks[i]) {
                if num_on_top_of[j] == 1 {
                    safe_to_disintegrate = false;
                    break;
                }
            }
        }
        if safe_to_disintegrate {
            num_can_be_disintegrated += 1;
        }
    }
    num_can_be_disintegrated
}
