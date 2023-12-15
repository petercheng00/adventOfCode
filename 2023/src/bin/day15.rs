use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut sum = 0;
    for step in input.trim_end().split(',') {
        sum += hash(step);
    }
    println!("Part 1: {}", sum);
}

fn hash(s: &str) -> u32 {
    let mut current = 0;
    for c in s.chars() {
        current += c as u32;
        current *= 17;
        current %= 256;
    }
    current
}

#[derive(Clone, Debug)]
struct Lens {
    label: String,
    focal_length: u8,
}

type Boxes = Vec<Vec<Lens>>;

fn part2(input: &str) {
    let mut boxes: Boxes = vec![vec![]; 256];
    for step in input.trim_end().split(',') {
        do_step(&mut boxes, step);
    }
    let mut sum_focus_power = 0;
    for (box_index, lens_box) in boxes.iter().enumerate() {
        let box_num = 1 + box_index;
        for (lens_index, lens) in lens_box.iter().enumerate() {
            let lens_num = 1 + lens_index;
            sum_focus_power += box_num * lens_num * lens.focal_length as usize;
        }
    }
    println!("Part 2: {}", sum_focus_power);
}

fn do_step(boxes: &mut Boxes, step: &str) {
    if let Some(label) = step.strip_suffix('-') {
        let lens_box = &mut boxes[hash(label) as usize];
        if let Some(lens_index) = lens_box.iter_mut().position(|lens| lens.label == label) {
            lens_box.remove(lens_index);
        }
    } else {
        let (label, focal_length) = step.split_once('=').unwrap();
        let focal_length = focal_length.parse::<u8>().unwrap();
        let lens_box = &mut boxes[hash(label) as usize];
        if let Some(lens) = lens_box.iter_mut().find(|lens| lens.label == label) {
            lens.focal_length = focal_length;
        } else {
            lens_box.push(Lens {
                label: label.to_string(),
                focal_length,
            });
        }
    }
}
