use std::env;
use std::fs;

use nalgebra::{Matrix2, Vector2, Vector3};

pub fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let filename = args.get(1).expect("Provide an input filename.");

    fs::read_to_string(filename).expect("Should have been able to read the file")
}

pub type Vec2 = Vector2<i64>;
pub type Mat2 = Matrix2<i64>;

pub const LEFT: Vec2 = Vec2::new(-1, 0);
pub const RIGHT: Vec2 = Vec2::new(1, 0);
pub const UP: Vec2 = Vec2::new(0, -1);
pub const DOWN: Vec2 = Vec2::new(0, 1);

pub const DIRS: [Vec2; 4] = [LEFT, RIGHT, UP, DOWN];

pub type Vec3 = Vector3<i64>;
