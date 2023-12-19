use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let (grid, start_xy) = load_input(input);

    for d in DIRECTIONS {
        if let Some(loop_pipes) = find_loop_from(&grid, start_xy, d) {
            println!("Part 1: {:?}", loop_pipes.len() / 2);
            return;
        }
    }
}

type Direction = (i8, i8);
const NORTH: Direction = (0, -1);
const EAST: Direction = (1, 0);
const SOUTH: Direction = (0, 1);
const WEST: Direction = (-1, 0);
const DIRECTIONS: [Direction; 4] = [NORTH, EAST, SOUTH, WEST];

const VALID_PIPES: [char; 6] = ['|', '-', 'L', 'J', '7', 'F'];

#[derive(Clone, Copy, Debug)]
struct Pipe {
    symbol: char,
}

impl Pipe {
    fn new(symbol: char) -> Option<Self> {
        if VALID_PIPES.contains(&symbol) {
            Some(Self { symbol })
        } else {
            None
        }
    }

    fn from_exits(exit1: Direction, exit2: Direction) -> Self {
        match (exit1, exit2) {
            (NORTH, SOUTH) => Self { symbol: '|' },
            (EAST, WEST) => Self { symbol: '-' },
            (NORTH, EAST) => Self { symbol: 'L' },
            (NORTH, WEST) => Self { symbol: 'J' },
            (SOUTH, WEST) => Self { symbol: '7' },
            (SOUTH, EAST) => Self { symbol: 'F' },
            (SOUTH, NORTH) => Self { symbol: '|' },
            (WEST, EAST) => Self { symbol: '-' },
            (EAST, NORTH) => Self { symbol: 'L' },
            (WEST, NORTH) => Self { symbol: 'J' },
            (WEST, SOUTH) => Self { symbol: '7' },
            (EAST, SOUTH) => Self { symbol: 'F' },
            _ => panic!("Invalid exits"),
        }
    }

    fn exits(&self) -> (Direction, Direction) {
        match self.symbol {
            '|' => (NORTH, SOUTH),
            '-' => (EAST, WEST),
            'L' => (NORTH, EAST),
            'J' => (NORTH, WEST),
            '7' => (SOUTH, WEST),
            'F' => (SOUTH, EAST),
            _ => panic!("Invalid pipe symbol"),
        }
    }

    fn traverse(&self, incoming_direction: Direction) -> Option<Direction> {
        let (exit1, exit2) = self.exits();
        if exit1 == incoming_direction {
            Some(exit2)
        } else if exit2 == incoming_direction {
            Some(exit1)
        } else {
            None
        }
    }
}

#[derive(Clone)]
struct Grid {
    data: Vec<Vec<Option<Pipe>>>,
}

impl std::fmt::Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in &self.data {
            for pipe in row {
                if let Some(pipe) = pipe {
                    write!(f, "{}", pipe.symbol)?;
                } else {
                    write!(f, ".")?;
                }
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

impl Grid {
    fn get(&self, xy: (usize, usize)) -> Option<&Pipe> {
        self.data.get(xy.1)?.get(xy.0)?.as_ref()
    }
}

fn load_input(input: &str) -> (Grid, (usize, usize)) {
    let height = input.lines().count();
    let width = input.lines().next().unwrap().chars().count();

    let mut data = vec![vec![None; width]; height];
    let mut start_xy = None;

    for (row, line) in input.lines().enumerate() {
        for (col, symbol) in line.chars().enumerate() {
            if let Some(pipe) = Pipe::new(symbol) {
                data[row][col] = Some(pipe);
            } else if symbol == 'S' {
                start_xy = Some((col, row));
            }
        }
    }
    (Grid { data }, start_xy.unwrap())
}

fn find_loop_from(
    grid: &Grid,
    start_xy: (usize, usize),
    start_direction: Direction,
) -> Option<Vec<(usize, usize)>> {
    let mut loop_pipes = vec![start_xy];
    let mut current_xy = start_xy;
    let mut current_direction = start_direction;

    loop {
        let next_xy = (
            current_xy.0 + current_direction.0 as usize,
            current_xy.1 + current_direction.1 as usize,
        );
        if next_xy == start_xy {
            // Found a loop.
            break;
        }

        let next_pipe = grid.get(next_xy)?;
        let incoming_direction = (-current_direction.0, -current_direction.1);
        let outgoing_direction = next_pipe.traverse(incoming_direction)?;

        loop_pipes.push(next_xy);
        current_xy = next_xy;
        current_direction = outgoing_direction;
    }

    Some(loop_pipes)
}

fn part2(input: &str) {
    // Redo part1.
    let (grid, start_xy) = load_input(input);

    let mut loop_pipes = None;
    for d in DIRECTIONS {
        loop_pipes = find_loop_from(&grid, start_xy, d);
        if loop_pipes.is_some() {
            break;
        }
    }
    let loop_pipes = loop_pipes.unwrap();

    // Remove all the other pipes.
    let mut clean_grid = grid.clone();
    for row in clean_grid.data.iter_mut() {
        for col in row {
            *col = None;
        }
    }
    for &xy in &loop_pipes {
        clean_grid.data[xy.1][xy.0] = grid.get(xy).cloned();
    }
    println!("{}", clean_grid);

    // Now we need to add in the right pipe for the start position.
    let exit1 = (
        (loop_pipes[1].0 as i32 - start_xy.0 as i32) as i8,
        (loop_pipes[1].1 as i32 - start_xy.1 as i32) as i8,
    );
    let exit2 = (
        (loop_pipes.last().unwrap().0 as i32 - start_xy.0 as i32) as i8,
        (loop_pipes.last().unwrap().1 as i32 - start_xy.1 as i32) as i8,
    );
    let start_pipe = Pipe::from_exits(exit1, exit2);
    clean_grid.data[start_xy.1][start_xy.0] = Some(start_pipe);
    println!("{}", clean_grid);

    // Scan row by row tracking winding.
    let mut total_inside = 0;
    for (_row, row_pipes) in clean_grid.data.iter().enumerate() {
        let mut current_inside = false;
        let mut col = 0;
        while col < row_pipes.len() {
            let Some(pipe) = &row_pipes[col] else {
                // No pipe here means add to count if we're inside.
                if current_inside {
                    total_inside += 1;
                }
                col += 1;
                continue;
            };
            // Since we're hardcoded scanning east, we can just hardcode the checks.
            match pipe.symbol {
                '|' => {
                    // This is a wall, swap inside-ness.
                    current_inside = !current_inside;
                    col += 1;
                }
                'F' => {
                    // We'll hit '-'s until we eventually hit either a '7' or a 'J'.
                    // '7' means don't change inside-ness, 'J' means do change.
                    loop {
                        col += 1;
                        // Should always be '-' pipes until we hit a 7 or a J
                        let pipe = row_pipes[col].unwrap();
                        if pipe.symbol == '7' {
                            col += 1;
                            break;
                        } else if pipe.symbol == 'J' {
                            current_inside = !current_inside;
                            col += 1;
                            break;
                        }
                        assert_eq!(pipe.symbol, '-');
                    }
                }
                'L' => {
                    // Same as above, except '7' is swap and 'J' is don't.
                    // Should always be '-' pipes until we hit a 7 or a J
                    loop {
                        col += 1;
                        let pipe = row_pipes[col].unwrap();
                        if pipe.symbol == '7' {
                            current_inside = !current_inside;
                            col += 1;
                            break;
                        } else if pipe.symbol == 'J' {
                            col += 1;
                            break;
                        }
                        assert_eq!(pipe.symbol, '-');
                    }
                }
                _ => {
                    panic!("Impossible to hit any other pipe symbol here!");
                }
            }
        }
    }
    println!("Total inside: {}", total_inside);
}
