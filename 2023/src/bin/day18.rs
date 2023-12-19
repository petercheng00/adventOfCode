use std::collections::HashMap;

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    do_everything(input);
}

fn part2(input: &str) {
    let mut new_input = String::new();
    for line in input.lines() {
        let hex_str = line.split_ascii_whitespace().last().unwrap();
        let hex_str = hex_str
            .strip_prefix("(#")
            .unwrap()
            .strip_suffix(")")
            .unwrap();
        let last_char = hex_str.chars().last().unwrap();
        let dir_char = match last_char {
            '0' => 'R',
            '1' => 'D',
            '2' => 'L',
            '3' => 'U',
            _ => panic!("Invalid direction"),
        };
        let hex_str = &hex_str[..hex_str.len() - 1];
        let hex_num = i32::from_str_radix(hex_str, 16).unwrap();
        new_input.push_str(&format!("{} {}\n", dir_char, hex_num));
    }
    do_everything(new_input.as_str());
}

fn do_everything(input: &str) {
    let mut y_to_segments = HashMap::<i64, Vec<(i64, i64)>>::new();
    let mut current_xy = Vec2::new(0, 0);
    for line in input.lines() {
        let mut split = line.split_whitespace();
        let dir = split.next().unwrap();
        let amount = split.next().unwrap().parse::<i64>().unwrap();

        let dir = match dir {
            "U" => UP,
            "D" => DOWN,
            "L" => LEFT,
            "R" => RIGHT,
            _ => panic!("Invalid direction"),
        };

        let next_xy = current_xy + dir * amount;

        if dir == LEFT || dir == RIGHT {
            let x1 = current_xy.x.min(next_xy.x);
            let x2 = current_xy.x.max(next_xy.x);
            y_to_segments
                .entry(current_xy.y)
                .or_insert_with(Vec::new)
                .push((x1, x2));
        }
        current_xy = next_xy;
    }
    assert!(current_xy.x == 0 && current_xy.y == 0);

    let mut y_values = y_to_segments.keys().copied().collect::<Vec<_>>();
    y_values.sort();

    let mut prev_y = *y_values.first().unwrap();
    let mut active_segments = y_to_segments.get(&prev_y).unwrap().clone();

    let mut sum_area = 0;
    for &y in y_values.iter().skip(1) {
        let prev_y_height = y - prev_y + 1;
        let prev_area = active_segments
            .iter()
            .map(|(x1, x2)| (x2 - x1 + 1) * prev_y_height)
            .sum::<i64>();

        let next_segments = y_to_segments.get(&y).unwrap();

        let (merged_segments, intersection_len) = merge_segments(&active_segments, next_segments);

        sum_area += prev_area - intersection_len;

        prev_y = y;
        active_segments = merged_segments;
    }
    println!("sum_area: {}", sum_area);
}

fn merge_segments(
    active_segments: &[(i64, i64)],
    next_segments: &[(i64, i64)],
) -> (Vec<(i64, i64)>, i64) {
    let mut segments = active_segments.clone().to_vec();

    // Each next segment can
    // 0. If it doesn't interact with any segments, create a new one!
    // 1. not interact with an active segment at all
    // 2. destroy the active segment if x1==x1 and x2==x2
    // 3. shrink the active segment if x1==x1 or x2==x2
    // 4. grow the active segment if x1==x2 or x2==x1
    // 5. split the active segment if fully enclosed.
    // argument: should not be possible for intersection that crosses an endpoint.

    // Also track the length of the intersection, which we'll subtract as the double counted area.
    // It starts as the sum of the active segments.
    let mut intersection_len = active_segments
        .iter()
        .map(|(x1, x2)| (x2 - x1 + 1))
        .sum::<i64>();
    for next in next_segments {
        let mut interacted = false;
        for s in &mut segments {
            if s.0 == s.1 {
                // Already destroyed.
            } else if s.0 > next.1 || s.1 < next.0 {
                // No overlap
            } else if s.0 == next.0 && s.1 == next.1 {
                // destroy
                intersection_len -= s.1 - s.0 + 1;
                s.0 = s.1;
                interacted = true;
                break;
            } else if s.0 == next.0 {
                // shrink
                intersection_len -= next.1 - s.0;
                s.0 = next.1;
                interacted = true;
                break;
            } else if s.1 == next.1 {
                // shrink
                intersection_len -= s.1 - next.0;
                s.1 = next.0;
                interacted = true;
                break;
            } else if s.1 == next.0 {
                // grow
                s.1 = next.1;
                interacted = true;
                break;
            } else if s.0 == next.1 {
                // grow
                s.0 = next.0;
                interacted = true;
                break;
            } else if s.0 < next.0 && s.1 > next.1 {
                // split into (s.0, next.0) and (next.1, s.1)
                intersection_len -= next.1 - next.0 - 1;
                let s1 = s.1;
                s.1 = next.0;
                segments.push((next.1, s1));
                interacted = true;
                break;
            } else {
                println!("s: {:?} next: {:?}", s, next);
                panic!("Unexpected interaction");
            }
        }
        if !interacted {
            segments.push(*next);
        }
    }
    // Glue together any segments that are adjacent.
    let mut keep_going = true;
    while keep_going {
        keep_going = false;
        for i in 0..segments.len() {
            if segments[i].0 == segments[i].1 {
                continue;
            }
            for j in 0..segments.len() {
                if segments[j].0 == segments[j].1 {
                    continue;
                }
                if i == j {
                    continue;
                }
                if segments[i].1 == segments[j].0 {
                    // Merge into segment i and destroy segment j.
                    segments[i].1 = segments[j].1;
                    segments[j].0 = segments[j].1;
                    keep_going = true;
                }
            }
        }
    }

    // Remove the destroyed segments.
    segments.retain(|s| s.0 < s.1);
    (segments, intersection_len)
}
