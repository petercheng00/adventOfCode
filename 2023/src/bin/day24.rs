use aoc2023_rust::*;
use nalgebra as na;
use rmpfit::{mpfit, MPFitter, MPResult, MPStatus};

// const TEST_RANGE: (u64, u64) = (7, 27);
const TEST_RANGE: (u64, u64) = (200000000000000, 400000000000000);

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let hailstones = load_hailstones(input);
    let mut count = 0;
    for i in 0..hailstones.len() {
        for j in i + 1..hailstones.len() {
            let a = &hailstones[i];
            let b = &hailstones[j];
            if let Some(xy) = intersection(a, b) {
                if xy.x >= TEST_RANGE.0 as f64
                    && xy.x <= TEST_RANGE.1 as f64
                    && xy.y >= TEST_RANGE.0 as f64
                    && xy.y <= TEST_RANGE.1 as f64
                {
                    count += 1;
                }
            }
        }
    }
    println!("Part 1: {}", count);
}

fn intersection(a: &Hailstone, b: &Hailstone) -> Option<na::Vector2<f64>> {
    // p1.x + v1.x * t1 = p2.x + v2.x * t2
    // p1.y + v1.y * t1 = p2.y + v2.y * t2

    // v1.x * t1 - v2.x * t2 = p2.x - p1.x
    // v1.y * t1 - v2.y * t2 = p2.y - p1.y

    // [v1.x, -v2.x] * [t1] = [p2.x - p1.x]
    // [v1.y, -v2.y]   [t2]   [p2.y - p1.y]

    let a_mat = na::Matrix2::new(a.velocity.x, -b.velocity.x, a.velocity.y, -b.velocity.y);
    let b_mat = na::Vector2::new(b.position.x - a.position.x, b.position.y - a.position.y);
    let t = a_mat.try_inverse()? * b_mat;

    if t[0] < 0.0 || t[1] < 0.0 {
        return None;
    }

    let x = a.position.x + a.velocity.x * t[0];
    let y = a.position.y + a.velocity.y * t[0];

    Some(na::Vector2::new(x, y))
}

#[derive(Debug)]
struct Hailstone {
    position: na::Vector3<f64>,
    velocity: na::Vector3<f64>,
}

fn load_hailstones(input: &str) -> Vec<Hailstone> {
    let mut hailstones = Vec::new();
    for line in input.lines() {
        let (pos_str, vel_str) = line.split_once(" @").unwrap();
        let mut pos_iter = pos_str.split(",").map(|s| s.trim().parse::<i64>().unwrap());
        let position = na::Vector3::new(
            pos_iter.next().unwrap() as f64,
            pos_iter.next().unwrap() as f64,
            pos_iter.next().unwrap() as f64,
        );
        let mut vel_iter = vel_str.split(",").map(|s| s.trim().parse::<i64>().unwrap());
        let velocity = na::Vector3::new(
            vel_iter.next().unwrap() as f64,
            vel_iter.next().unwrap() as f64,
            vel_iter.next().unwrap() as f64,
        );
        hailstones.push(Hailstone { position, velocity });
    }
    hailstones
}

fn part2(input: &str) {
    let hailstones = load_hailstones(input);

    // p1.x + v1.x * t1 - rpx - rvx * t1 = 0
    // t1 (v1.x - rvx) = rpx - p1.x
    // t1 = (rpx - p1.x) / (v1.x - rvx)
    // (rpx - p1.x) / (v1.x - rvx) = (rpy - p1.y) / (v1.y - rvy)
    // (rpx - p1.x) * (v1.y - rvy) = (rpy - p1.y) * (v1.x - rvx)
    // (rpx - p1.x) * (v1.y - rvy) - (rpy - p1.y) * (v1.x - rvx) = 0
    // (rpx - p1.x) * (v1.z - rvz) - (rpz - p1.z) * (v1.x - rvx) = 0
    // The above 2 equations exist for each hailstone, 6 unknowns to solve.

    let problem = HailstonesProblem { hailstones };
    let mut init = [1000000.0; 6];
    let res = mpfit(&problem, &mut init, None, &Default::default());
    println!("{:?}", res.is_ok());
    println!("{:?}", init);
    println!("Part 2: {}", init[0] + init[1] + init[2]);
}

struct HailstonesProblem {
    hailstones: Vec<Hailstone>,
}

impl MPFitter for HailstonesProblem {
    fn number_of_points(&self) -> usize {
        // 2 residuals per hailstone.
        self.hailstones.len() * 2
    }

    fn eval(&self, params: &[f64], deviates: &mut [f64]) -> MPResult<()> {
        for (i, hailstone) in self.hailstones.iter().enumerate() {
            let rpx = params[0];
            let rpy = params[1];
            let rpz = params[2];
            let rvx = params[3];
            let rvy = params[4];
            let rvz = params[5];
            let px = hailstone.position.x;
            let py = hailstone.position.y;
            let pz = hailstone.position.z;
            let vx = hailstone.velocity.x;
            let vy = hailstone.velocity.y;
            let vz = hailstone.velocity.z;

            deviates[i * 2] = (rpx - px) * (vy - rvy) - (rpy - py) * (vx - rvx);
            deviates[i * 2 + 1] = (rpx - px) * (vz - rvz) - (rpz - pz) * (vx - rvx);
        }
        Ok(())
    }
}
