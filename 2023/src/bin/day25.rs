use std::collections::HashSet;

use aoc2023_rust::*;
use rand::Rng;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut edges = vec![];
    let mut node_names = HashSet::new();
    for line in input.lines() {
        let (a, rest) = line.split_once(": ").unwrap();
        let a = a.to_string();
        for b in rest.split_whitespace() {
            edges.push((a.clone(), b.to_string()));
            node_names.insert(a.clone());
            node_names.insert(b.to_string());
        }
    }
    let num_nodes = node_names.len();
    while !try_kargers(&edges, num_nodes, 3) {}
}

fn part2(input: &str) {}

fn try_kargers(edges: &[(String, String)], num_nodes: usize, target: usize) -> bool {
    let mut edges = edges.to_vec();
    let mut num_nodes = num_nodes;
    let mut rng = rand::thread_rng();
    while num_nodes > 2 {
        let i = rng.gen_range(0..edges.len());
        // Remove the edge a-b.
        let (a, b) = edges[i].clone();
        let new_node_name = format!("{}-{}", a, b);
        // For each c-d edge, if it's the same as a-b, remove it.
        // Otherwise, if one end shares the name with a or b, change it to the new name.
        edges.retain_mut(|(c, d)| {
            if *c == a && *d == b || *c == b && *d == a {
                false
            } else {
                if *c == a || *c == b {
                    *c = new_node_name.clone();
                }
                if *d == a || *d == b {
                    *d = new_node_name.clone();
                }
                true
            }
        });

        num_nodes -= 1;
    }
    if edges.len() == target {
        let edge = &edges[0];
        let left_num_components = edge.0.matches('-').count() + 1;
        let right_num_components = edge.1.matches('-').count() + 1;
        println!(
            "Product is {} * {} = {}",
            left_num_components,
            right_num_components,
            left_num_components * right_num_components
        );
        return true;
    }
    false
}
