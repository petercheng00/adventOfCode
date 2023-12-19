use std::collections::HashMap;

use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut sum_ways = 0;
    for line in input.lines() {
        let (row, groups) = parse_line(line);
        let mut cache = HashMap::<(usize, usize, bool), u64>::new();
        let num_ways = get_num_ways(&row, &groups, &mut cache, 0, 0, true);
        sum_ways += num_ways;
    }
    println!("Part 1: {}", sum_ways);
}

fn parse_line(line: &str) -> (Vec<char>, Vec<usize>) {
    let (row_str, groups_str) = line.split_once(' ').unwrap();
    let row = row_str.chars().collect();
    let groups = groups_str
        .split(',')
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
    (row, groups)
}

/// Number of ways to find groups in row.
fn get_num_ways(
    chars: &[char],
    groups: &[usize],
    cache: &mut HashMap<(usize, usize, bool), u64>,
    char_index: usize,
    group_index: usize,
    can_start_block: bool,
) -> u64 {
    if let Some(result) = cache.get(&(char_index, group_index, can_start_block)) {
        return *result;
    }

    let current_char = chars.get(char_index);
    let current_group = groups.get(group_index);

    if current_char.is_none() {
        // Done, good if no more groups left, bad otherwise.
        return if current_group.is_none() { 1 } else { 0 };
    }
    let current_char = *current_char.unwrap();

    let sum_groups_left = groups[group_index..].iter().sum();
    let num_chars_left = chars.len() - char_index;
    if num_chars_left < sum_groups_left {
        // Not enough space to hold all the groups.
        // Technically we also have to leave 1 space between all the groups but whatever.
        return 0;
    }

    if current_char == '.' {
        // Nothing to do here, move on.
        let result = get_num_ways(chars, groups, cache, char_index + 1, group_index, true);
        cache.insert((char_index, group_index, can_start_block), result);
        return result;
    }
    if current_char == '#' {
        if !can_start_block || current_group.is_none() {
            // Can't start a block here, failed!
            cache.insert((char_index, group_index, can_start_block), 0);
            return 0;
        }
        let current_group = *current_group.unwrap();
        // Check if the next set of characters can match a group.
        let possible = chars[char_index..char_index + current_group]
            .iter()
            .all(|c| *c == '#' || *c == '?');
        if !possible {
            cache.insert((char_index, group_index, can_start_block), 0);
            return 0;
        }
        // Consume the next block. Next iteration can't start a block!
        let result = get_num_ways(
            chars,
            groups,
            cache,
            char_index + current_group,
            group_index + 1,
            false,
        );
        cache.insert((char_index, group_index, can_start_block), result);
        return result;
    }
    if current_char == '?' {
        // One option is to do nothing.
        let mut ways = get_num_ways(chars, groups, cache, char_index + 1, group_index, true);
        if !can_start_block || current_group.is_none() {
            // Can't start a block here, so just move on.
            cache.insert((char_index, group_index, can_start_block), ways);
            return ways;
        }
        let current_group = *current_group.unwrap();
        // Other option is to consume a block if possible.
        let consume_possible = chars[char_index..char_index + current_group]
            .iter()
            .all(|c| *c == '#' || *c == '?');
        if consume_possible {
            ways += get_num_ways(
                chars,
                groups,
                cache,
                char_index + current_group,
                group_index + 1,
                false,
            );
        }
        cache.insert((char_index, group_index, can_start_block), ways);
        return ways;
    }

    panic!("Can't get here!");
}

fn part2(input: &str) {
    let mut sum_ways = 0;
    for line in input.lines() {
        // String shenanigans.
        let (first, second) = line.split_once(' ').unwrap();
        let first5 = vec![first; 5].join("?");
        let second5 = vec![second; 5].join(",");
        let big_str = format!("{} {}", first5, second5);
        let (row, groups) = parse_line(&big_str);
        let mut cache = HashMap::<(usize, usize, bool), u64>::new();
        let num_ways = get_num_ways(&row, &groups, &mut cache, 0, 0, true);
        sum_ways += num_ways;
    }
    println!("Part 2: {}", sum_ways);
}
