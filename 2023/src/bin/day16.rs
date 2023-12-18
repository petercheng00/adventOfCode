use std::collections::HashSet;

use ndarray::Array2;

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let grid = Grid::new(input);
    let start_beam = Beam {
        xy: Vec2::new(0, 0),
        dir: RIGHT,
    };
    println!("Part 1: {}", grid.get_energized(start_beam));
}

fn part2(input: &str) {
    let mut max_energized = 0;
    let grid = Grid::new(input);
    // Top
    for x in 0..grid.data.shape()[1] {
        let start_beam = Beam {
            xy: Vec2::new(x as i32, 0),
            dir: DOWN,
        };
        max_energized = max_energized.max(grid.get_energized(start_beam));
    }
    // Left
    for y in 0..grid.data.shape()[0] {
        let start_beam = Beam {
            xy: Vec2::new(0, y as i32),
            dir: RIGHT,
        };
        max_energized = max_energized.max(grid.get_energized(start_beam));
    }
    // Right
    for y in 0..grid.data.shape()[0] {
        let start_beam = Beam {
            xy: Vec2::new(grid.data.shape()[1] as i32 - 1, y as i32),
            dir: LEFT,
        };
        max_energized = max_energized.max(grid.get_energized(start_beam));
    }
    // Bottom
    for x in 0..grid.data.shape()[1] {
        let start_beam = Beam {
            xy: Vec2::new(x as i32, grid.data.shape()[0] as i32 - 1),
            dir: UP,
        };
        max_energized = max_energized.max(grid.get_energized(start_beam));
    }
    println!("Part 2: {}", max_energized);
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Beam {
    xy: Vec2,
    dir: Vec2,
}

#[derive(Debug)]
struct Grid {
    data: Array2<char>,
}

impl Grid {
    fn new(input: &str) -> Self {
        let lines = input.lines().collect::<Vec<_>>();
        let shape = (lines.len(), lines[0].len());
        Self {
            data: Array2::from_shape_fn(shape, |(i, j)| lines[i].chars().nth(j).unwrap()),
        }
    }

    fn get(&self, xy: &Vec2) -> char {
        self.data[[xy.y as usize, xy.x as usize]]
    }

    fn in_bounds(&self, xy: &Vec2) -> bool {
        xy.x >= 0
            && xy.y >= 0
            && xy.x < self.data.shape()[1] as i32
            && xy.y < self.data.shape()[0] as i32
    }

    fn get_energized(&self, start_beam: Beam) -> usize {
        let mut active_beams = vec![start_beam];
        let mut processed_beams = HashSet::new();

        while let Some(beam) = active_beams.pop() {
            if processed_beams.contains(&beam) {
                continue;
            }

            for out_dir in self.process_beam(&beam) {
                let new_xy = beam.xy + out_dir;
                if self.in_bounds(&new_xy) {
                    active_beams.push(Beam {
                        xy: new_xy,
                        dir: out_dir,
                    });
                }
            }

            processed_beams.insert(beam);
        }

        let mut energized_tiles = HashSet::new();
        for beam in processed_beams {
            energized_tiles.insert(beam.xy);
        }
        energized_tiles.len()
    }

    fn process_beam(&self, beam: &Beam) -> Vec<Vec2> {
        match self.get(&beam.xy) {
            '.' => {
                // Just pass through
                vec![beam.dir]
            }
            '/' => {
                // Flip across diagonal.
                vec![Mat2::new(0, -1, -1, 0) * beam.dir]
            }
            '\\' => {
                // Flip across the other diagonal.
                vec![Mat2::new(0, 1, 1, 0) * beam.dir]
            }
            '|' => {
                if beam.dir == LEFT || beam.dir == RIGHT {
                    // Split up and down.
                    vec![UP, DOWN]
                } else {
                    // Pass through.
                    vec![beam.dir]
                }
            }
            '-' => {
                if beam.dir == UP || beam.dir == DOWN {
                    // Split left and right.
                    vec![LEFT, RIGHT]
                } else {
                    // Pass through.
                    vec![beam.dir]
                }
            }
            _ => panic!("Unexpected grid element!"),
        }
    }
}
