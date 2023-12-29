use std::collections::{HashMap, HashSet};

use aoc2023_rust::*;

use ndarray::Array2;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let grid = load_grid(input);
    let mut start_x = 0;
    for x in 0..grid.shape()[1] {
        if grid[[0, x]] == '.' {
            start_x = x;
            break;
        }
    }
    let mut end_x = 0;
    for x in 0..grid.shape()[1] {
        if grid[[grid.shape()[0] - 1, x]] == '.' {
            end_x = x;
            break;
        }
    }
    let start = Vec2::new(start_x as i64, 0);
    let end = Vec2::new(end_x as i64, grid.shape()[0] as i64 - 1);
    let history = vec![];

    println!(
        "Part 1: {}",
        max_steps(&grid, &start, &end, &history).unwrap()
    );
}

fn load_grid(input: &str) -> Array2<char> {
    let lines = input.lines().collect::<Vec<_>>();
    let shape = (lines.len(), lines[0].len());
    Array2::from_shape_fn(shape, |(i, j)| lines[i].chars().nth(j).unwrap())
}

fn max_steps(grid: &Array2<char>, current: &Vec2, end: &Vec2, history: &Vec<Vec2>) -> Option<i64> {
    if current == end {
        return Some(0);
    }

    let c = grid[[current.y as usize, current.x as usize]];
    let possible_dirs = match c {
        '.' => vec![UP, DOWN, LEFT, RIGHT],
        '^' => vec![UP],
        'v' => vec![DOWN],
        '<' => vec![LEFT],
        '>' => vec![RIGHT],
        _ => panic!("Unexpected char {}", c),
    };

    let mut best = None;
    let mut new_history = history.clone();
    new_history.push(current.clone());
    for dir in possible_dirs {
        let new_xy = current + dir;
        if !in_bounds(grid, &new_xy) {
            continue;
        }
        if grid[[new_xy.y as usize, new_xy.x as usize]] == '#' {
            continue;
        }
        if history.contains(&new_xy) {
            continue;
        }
        if let Some(possible) = max_steps(grid, &new_xy, end, &new_history) {
            if best.is_none() || possible + 1 > best.unwrap() {
                best = Some(possible + 1);
            }
        }
    }
    best
}

fn in_bounds(grid: &Array2<char>, xy: &Vec2) -> bool {
    xy.x >= 0 && xy.x < grid.shape()[1] as i64 && xy.y >= 0 && xy.y < grid.shape()[0] as i64
}

fn part2(input: &str) {
    let mut grid = load_grid(input);
    let mut start_x = 0;
    for x in 0..grid.shape()[1] {
        if grid[[0, x]] == '.' {
            start_x = x;
            break;
        }
    }
    let mut end_x = 0;
    for x in 0..grid.shape()[1] {
        if grid[[grid.shape()[0] - 1, x]] == '.' {
            end_x = x;
            break;
        }
    }
    let start = Vec2::new(start_x as i64, 0);
    let end = Vec2::new(end_x as i64, grid.shape()[0] as i64 - 1);

    // Replace all the slopes with '.'
    grid.iter_mut().for_each(|c| {
        if *c != '#' {
            *c = '.';
        }
    });

    // Nodes are start, end, and all the intersections.
    let mut nodes = vec![start, end];
    grid[[start.y as usize, start.x as usize]] = 'O';
    grid[[end.y as usize, end.x as usize]] = 'O';

    // Find all the branch points, and replace with 'O'.
    let (height, width) = grid.dim();
    for y in 0..height {
        for x in 0..width {
            if grid[[y, x]] == '#' {
                continue;
            }
            let mut num_paths = 0;
            for dir in DIRS {
                let new_xy = Vec2::new(x as i64, y as i64) + dir;
                if in_bounds(&grid, &new_xy) && grid[[new_xy.y as usize, new_xy.x as usize]] == '.'
                {
                    num_paths += 1;
                }
            }
            if num_paths > 2 {
                grid[[y, x]] = 'O';
                nodes.push(Vec2::new(x as i64, y as i64));
            }
        }
    }

    let graph = build_graph(&grid, &nodes);
    println!(
        "Part 2: {}",
        find_longest_path_to_end(&graph, &start, &end, &HashSet::new()).unwrap()
    );
}

fn build_graph(grid: &Array2<char>, nodes: &Vec<Vec2>) -> HashMap<Vec2, Vec<(Vec2, i64)>> {
    let mut graph = HashMap::new();
    for node in nodes {
        graph.insert(node.clone(), Vec::new());
    }
    let mut visited = HashSet::new();
    for node in nodes {
        visited.insert(node.clone());
        for dir in DIRS {
            let start = node + dir;
            if in_bounds(grid, &start)
                && grid[[start.y as usize, start.x as usize]] != '#'
                && !visited.contains(&start)
            {
                if let Some((end_node, steps)) = find_edge_end(grid, &start, 1, &mut visited) {
                    graph.get_mut(node).unwrap().push((end_node, steps));
                    graph.get_mut(&end_node).unwrap().push((*node, steps));
                }
            }
        }
    }
    graph
}

fn find_edge_end(
    grid: &Array2<char>,
    current: &Vec2,
    steps_so_far: i64,
    visited: &mut HashSet<Vec2>,
) -> Option<(Vec2, i64)> {
    if grid[[current.y as usize, current.x as usize]] == 'O' {
        // Done.
        return Some((current.clone(), steps_so_far));
    }
    visited.insert(current.clone());
    for dir in DIRS {
        let next = current + dir;
        if in_bounds(grid, &next)
            && grid[[next.y as usize, next.x as usize]] != '#'
            && !visited.contains(&next)
        {
            return find_edge_end(grid, &next, steps_so_far + 1, visited);
        }
    }
    panic!("Hit a dead end at {:?} - do these exist?", current);
    None
}

fn find_longest_path_to_end(
    graph: &HashMap<Vec2, Vec<(Vec2, i64)>>,
    current: &Vec2,
    end: &Vec2,
    visited: &HashSet<Vec2>,
) -> Option<i64> {
    if current == end {
        return Some(0);
    }
    let mut best = None;
    for (next, steps) in graph.get(current).unwrap() {
        if visited.contains(next) {
            continue;
        }
        let mut new_visited = visited.clone();
        new_visited.insert(next.clone());
        if let Some(possible) = find_longest_path_to_end(graph, next, end, &new_visited) {
            if best.is_none() || possible + steps > best.unwrap() {
                best = Some(possible + steps);
            }
        }
    }
    best
}
