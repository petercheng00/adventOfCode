use std::collections::HashMap;

use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let (instructions, network) = parse_input(input);
    let instructions = instructions.chars().collect::<Vec<_>>();

    let mut steps = 0;
    let mut current = "AAA";
    while current != "ZZZ" {
        let instruction = instructions[steps % instructions.len()];
        let dsts = network.get(current).unwrap();
        current = if instruction == 'L' {
            dsts.0.as_str()
        } else {
            dsts.1.as_str()
        };
        steps += 1;
    }
    println!("Part 1: {}", steps);
}

fn part2(input: &str) {
    let (instructions, network) = parse_input(input);
    let instructions = instructions.chars().collect::<Vec<_>>();

    let starts = network
        .keys()
        .filter(|k| k.ends_with("A"))
        .collect::<Vec<_>>();

    let mut loops = vec![];
    for start in starts {
        let l = find_loop(&network, &instructions, start);
        println!("Loop: {:?}", l);
        loops.push(l);
    }

    let mut step = 0;
    loop {
        step = loops[0].next_z_step(step);
        if loops.iter().all(|l| l.step_ends_with_z(step)) {
            println!("Part 2: {}", step);
            return;
        }
    }
}

fn parse_input(input: &str) -> (String, HashMap<String, (String, String)>) {
    let lines = input.lines().collect::<Vec<_>>();
    let instructions = lines[0].into();

    let mut network = HashMap::new();
    for line in lines.iter().skip(2) {
        let key = &line[0..=2];
        let value1 = &line[7..=9];
        let value2 = &line[12..=14];
        network.insert(key.into(), (value1.into(), value2.into()));
    }

    (instructions, network)
}

#[derive(Debug)]
struct Loop {
    start_step: usize,
    // If size is N, then step 0 == step N.
    size: usize,
    // start_step + these offsets all end in Z.
    end_with_z_offsets: Vec<usize>,
}

impl Loop {
    fn step_ends_with_z(&self, global_step: usize) -> bool {
        let step = (global_step - self.start_step) % self.size;
        self.end_with_z_offsets.contains(&step)
    }

    fn next_z_step(&self, global_step: usize) -> usize {
        if global_step < self.start_step {
            return self.start_step + self.end_with_z_offsets[0];
        }
        let step = (global_step - self.start_step) % self.size;
        for &offset in &self.end_with_z_offsets {
            if offset > step {
                return global_step + offset - step;
            }
        }
        // otherwise wrap around.
        global_step + self.size - step + self.end_with_z_offsets[0]
    }
}

fn find_loop(
    network: &HashMap<String, (String, String)>,
    instructions: &[char],
    start: &str,
) -> Loop {
    // At each step, store the node name.
    let mut trail = vec![start];
    let mut step = 0;
    loop {
        let instruction = instructions[step % instructions.len()];
        let dsts = network.get(&trail.last().unwrap().to_string()).unwrap();
        let dst = if instruction == 'L' {
            dsts.0.as_str()
        } else {
            dsts.1.as_str()
        };
        step += 1;
        for (i, &t) in trail.iter().enumerate() {
            if t == dst && (i % instructions.len()) == (step % instructions.len()) {
                let start_step = i;
                let size = step - i;
                println!(
                    "Found loop for start {}. Loops on {} from step {} -> {} (size {})",
                    start, dst, start_step, step, size
                );
                let mut end_with_z_offsets = vec![];
                for loop_step in start_step..step {
                    if trail[loop_step].ends_with("Z") {
                        end_with_z_offsets.push(loop_step - start_step);
                    }
                }
                return Loop {
                    start_step,
                    size,
                    end_with_z_offsets,
                };
            }
        }
        trail.push(dst);
    }
}
