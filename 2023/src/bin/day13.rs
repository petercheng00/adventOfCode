use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let patterns = load_patterns(input);
    let mut sum = 0;
    for pattern in patterns {
        if let Some(rows_above) = get_horizontal_reflection(&pattern) {
            sum += 100 * rows_above;
        } else {
            let transposed = transpose(&pattern);
            if let Some(cols_left) = get_horizontal_reflection(&transposed) {
                sum += cols_left;
            } else {
                panic!("failed!");
            }
        }
    }
    println!("Part 1: {}", sum);
}

fn part2(input: &str) {
    let patterns = load_patterns(input);
    let mut sum = 0;
    for pattern in patterns {
        if let Some(rows_above) = get_smudged_horizontal_reflection(&pattern) {
            sum += 100 * rows_above;
        } else {
            let transposed = transpose(&pattern);
            if let Some(cols_left) = get_smudged_horizontal_reflection(&transposed) {
                sum += cols_left;
            } else {
                panic!("failed!");
            }
        }
    }
    println!("Part 2: {}", sum);
}

type Pattern = Vec<Vec<char>>;

fn load_patterns(input: &str) -> Vec<Pattern> {
    let mut patterns = Vec::new();
    let mut current_pattern = Vec::new();
    for line in input.lines() {
        if line.is_empty() {
            patterns.push(current_pattern);
            current_pattern = Vec::new();
            continue;
        }
        let chars = line.chars().collect::<Vec<char>>();
        current_pattern.push(chars);
    }
    patterns.push(current_pattern);
    patterns
}

fn get_horizontal_reflection(pattern: &Pattern) -> Option<usize> {
    for split_row_above in 0..pattern.len() - 1 {
        let num_rows_above = split_row_above + 1;
        let num_rows_below = pattern.len() - num_rows_above;
        let mut good = true;
        for i in 0..num_rows_above.min(num_rows_below) {
            let above_row = &pattern[split_row_above - i];
            let below_row = &pattern[split_row_above + 1 + i];
            if above_row != below_row {
                good = false;
                break;
            }
        }
        if good {
            return Some(num_rows_above);
        }
    }
    None
}

fn transpose(pattern: &Pattern) -> Pattern {
    let mut transposed = vec![vec!['.'; pattern.len()]; pattern[0].len()];
    for row in 0..pattern.len() {
        for col in 0..pattern[0].len() {
            transposed[col][row] = pattern[row][col];
        }
    }
    transposed
}

fn get_smudged_horizontal_reflection(pattern: &Pattern) -> Option<usize> {
    for split_row_above in 0..pattern.len() - 1 {
        let num_rows_above = split_row_above + 1;
        let num_rows_below = pattern.len() - num_rows_above;
        let mut good = true;
        let mut changed_one = false;
        for i in 0..num_rows_above.min(num_rows_below) {
            let above_row = &pattern[split_row_above - i];
            let below_row = &pattern[split_row_above + 1 + i];

            let num_matches = above_row
                .iter()
                .zip(below_row.iter())
                .filter(|(a, b)| a == b)
                .count();

            if num_matches == above_row.len() {
                // A normal match.
                continue;
            }

            if num_matches == above_row.len() - 1 && !changed_one {
                // We can change one.
                changed_one = true;
                continue;
            }

            good = false;
            break;
        }
        if good && changed_one {
            return Some(num_rows_above);
        }
    }
    None
}
