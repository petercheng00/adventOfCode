use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    both_parts(&input_str, 2);
    both_parts(&input_str, 1000000);
}

fn both_parts(input: &str, expansion_factor: usize) {
    let mut grid = vec![];
    for line in input.lines() {
        let mut row = vec![];
        for c in line.chars() {
            row.push(c);
        }
        grid.push(row);
    }
    let mut empty_rows = vec![];
    for row in 0..grid.len() {
        if grid[row].iter().all(|&c| c == '.') {
            empty_rows.push(row);
        }
    }
    let mut empty_cols = vec![];
    for col in 0..grid[0].len() {
        if grid.iter().all(|row| row[col] == '.') {
            empty_cols.push(col);
        }
    }

    let mut raw_galaxy_rowcols = vec![];
    for row in 0..grid.len() {
        for col in 0..grid[0].len() {
            if grid[row][col] == '#' {
                raw_galaxy_rowcols.push((row, col));
            }
        }
    }

    let mut real_galaxy_rowcols = vec![];
    for (row, col) in raw_galaxy_rowcols {
        let add_rows = empty_rows.iter().filter(|&&r| r < row).count();
        let add_cols = empty_cols.iter().filter(|&&c| c < col).count();
        let add_rows = add_rows * (expansion_factor - 1);
        let add_cols = add_cols * (expansion_factor - 1);
        real_galaxy_rowcols.push((row + add_rows, col + add_cols));
    }

    let mut sum_dists = 0;
    for i in 0..real_galaxy_rowcols.len() {
        for j in i + 1..real_galaxy_rowcols.len() {
            let (row1, col1) = real_galaxy_rowcols[i];
            let (row2, col2) = real_galaxy_rowcols[j];
            let dist = (row1 as i64 - row2 as i64).abs() + (col1 as i64 - col2 as i64).abs();
            sum_dists += dist;
        }
    }
    println!("{}", sum_dists);
}
