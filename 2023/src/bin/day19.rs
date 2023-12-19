use std::collections::HashMap;

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let (workflows, parts) = parse_input(input);

    // All the parts start in "in".
    let mut queues = HashMap::new();
    for p in parts {
        queues.entry("in").or_insert(vec![]).push(p);
    }

    let mut keep_going = true;
    while keep_going {
        keep_going = false;
        for name in workflows.keys() {
            // for (&name, queue) in &mut queues {
            if matches!(name.as_str(), "A" | "R") {
                continue;
            }
            let queue = if let Some(q) = queues.get_mut(name.as_str()) {
                let q2 = q.clone();
                q.clear();
                q2
            } else {
                continue;
            };
            let rules = workflows.get(name).unwrap();
            'parts: for part in queue {
                for rule in rules {
                    if passes_rule(&part, rule) {
                        let dst = rule.dst.as_str();
                        queues.entry(dst).or_insert(vec![]).push(part.clone());
                        keep_going = true;
                        continue 'parts;
                    }
                }
                panic!("Failed all rules, shouldn't happen!");
            }
        }
    }
    let sum_accepted = queues
        .get("A")
        .unwrap()
        .iter()
        .map(|p| p.values().sum::<i32>())
        .sum::<i32>();
    println!("{}", sum_accepted);
}

fn part2(input: &str) {
    let (workflows, _parts) = parse_input(input);
    let mut min_part = Part::new();
    let mut max_part = Part::new();
    for c in ['x', 'm', 'a', 's'] {
        min_part.insert(c, 1);
        max_part.insert(c, 4000);
    }
    println!("{}", num_ways(&workflows, "in", min_part, max_part));
}

struct Rule {
    // If field is ' ' then this is a dummy rule that always passes.
    field: char,
    is_gt: bool,
    value: i32,
    dst: String,
}

type Part = HashMap<char, i32>;
type Workflows = HashMap<String, Vec<Rule>>;

fn parse_input(input: &str) -> (Workflows, Vec<Part>) {
    let mut workflows = Workflows::new();
    let mut parts = vec![];

    let mut done_rules = false;

    for line in input.lines() {
        if line.is_empty() {
            done_rules = true;
            continue;
        }
        if !done_rules {
            let (name, rules) = parse_rules(line);
            workflows.insert(name, rules);
        } else {
            parts.push(parse_part(line));
        }
    }
    (workflows, parts)
}

fn parse_rules(line: &str) -> (String, Vec<Rule>) {
    let (name, rules_str) = line.split_once("{").unwrap();
    let rules_str = rules_str.strip_suffix("}").unwrap();
    let mut rules = vec![];
    for rules_str in rules_str.split(",") {
        if !rules_str.contains(":") {
            rules.push(Rule {
                field: ' ',
                is_gt: false,
                value: 0,
                dst: rules_str.to_string(),
            });
            continue;
        }
        let (rules_str, dst) = rules_str.split_once(":").unwrap();
        let field = rules_str.chars().nth(0).unwrap();
        let is_gt = rules_str.chars().nth(1).unwrap() == '>';
        let value = rules_str[2..].parse::<i32>().unwrap();
        rules.push(Rule {
            field,
            is_gt,
            value,
            dst: dst.to_string(),
        });
    }
    (name.to_string(), rules)
}

fn parse_part(line: &str) -> Part {
    let mut part = Part::new();
    let line = line.strip_prefix("{").unwrap();
    let line = line.strip_suffix("}").unwrap();
    for part_str in line.split(",") {
        let field = part_str.chars().nth(0).unwrap();
        let value = part_str[2..].parse::<i32>().unwrap();
        part.insert(field, value);
    }
    part
}

fn passes_rule(part: &Part, rule: &Rule) -> bool {
    if rule.field == ' ' {
        return true;
    }
    let part_value = *part.get(&rule.field).unwrap();
    if rule.is_gt {
        part_value > rule.value
    } else {
        part_value <= rule.value
    }
}

/// Number of ways to end up at 'A', given all possible parts between min_part and max_part.
fn num_ways(workflows: &Workflows, current: &str, min_part: Part, max_part: Part) -> u64 {
    if current == "A" {
        let mut product = 1;
        for c in ['x', 'm', 'a', 's'] {
            let min_value = *min_part.get(&c).unwrap() as u64;
            let max_value = *max_part.get(&c).unwrap() as u64;
            product *= max_value - min_value + 1;
        }
        return product;
    }
    if current == "R" {
        return 0;
    }

    let mut min_part = min_part;
    let mut max_part = max_part;

    let mut sum_ways = 0;
    let rules = workflows.get(current).unwrap();
    for rule in rules {
        if rule.field == ' ' {
            // Everything goes into this rule.
            sum_ways += num_ways(workflows, &rule.dst, min_part.clone(), max_part.clone());
            break;
        }

        let min_value = *min_part.get(&rule.field).unwrap();
        let max_value = *max_part.get(&rule.field).unwrap();

        if rule.is_gt {
            if min_value > rule.value {
                // Everything goes into this rule.
                sum_ways += num_ways(workflows, &rule.dst, min_part.clone(), max_part.clone());
                break;
            } else if max_value <= rule.value {
                // Nothing goes into this rule.
                continue;
            } else {
                // Some goes into this rule, some continues onwards.
                let mut new_min_part = min_part.clone();
                new_min_part.insert(rule.field, rule.value + 1);
                sum_ways += num_ways(workflows, &rule.dst, new_min_part, max_part.clone());
                max_part.insert(rule.field, rule.value);
            }
        } else {
            if max_value < rule.value {
                // Everything goes into this rule.
                sum_ways += num_ways(workflows, &rule.dst, min_part.clone(), max_part.clone());
                break;
            } else if min_value >= rule.value {
                // Nothing goes into this rule.
                continue;
            } else {
                // Some goes into this rule, some continues onwards.
                let mut new_max_part = max_part.clone();
                new_max_part.insert(rule.field, rule.value - 1);
                sum_ways += num_ways(workflows, &rule.dst, min_part.clone(), new_max_part);
                min_part.insert(rule.field, rule.value);
            }
        }
    }
    sum_ways
}
