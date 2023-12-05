use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let lines = input.lines().collect::<Vec<_>>();
    let seeds = parse_seeds(lines[0]);
    let mut current_values = seeds;

    let mut line_num = 1;
    while line_num < lines.len() {
        let line = lines[line_num];
        if line.contains("map") {
            println!("Processing map {}", line);
            let (end_line_num, new_values) =
                parse_and_map_values(&lines, line_num, &current_values);
            line_num = end_line_num;
            current_values = new_values;
        }
        line_num += 1;
    }
    println!(
        "Min final value is {}",
        current_values.iter().min().unwrap()
    );
}

fn parse_seeds(line: &str) -> Vec<i64> {
    let mut seeds = vec![];
    for x in line.split(" ") {
        if let Ok(x) = x.parse::<i64>() {
            seeds.push(x);
        }
    }
    seeds
}

fn parse_and_map_values(
    lines: &Vec<&str>,
    line_num: usize,
    values: &Vec<i64>,
) -> (usize, Vec<i64>) {
    // First load the tuples of 3 numbers into mappings.
    let mut mappings = vec![];
    let mut line_num = line_num + 1;
    loop {
        let line = lines[line_num];
        if line.is_empty() {
            break;
        }
        let nums = line.split(" ").collect::<Vec<_>>();
        let nums = nums
            .iter()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<_>>();
        mappings.push((nums[0], nums[1], nums[2]));
        line_num += 1;
        if line_num >= lines.len() {
            break;
        }
    }

    let mut new_values = Vec::with_capacity(values.len());
    for &value in values {
        let mut successful_map = false;
        for (dst_start, src_start, range) in &mappings {
            if value >= *src_start && value < *src_start + *range {
                new_values.push(dst_start + value - src_start);
                successful_map = true;
            }
        }
        if !successful_map {
            new_values.push(value);
        }
    }
    (line_num, new_values)
}

fn part2(input: &str) {
    let lines = input.lines().collect::<Vec<_>>();
    let seed_ranges = parse_seed_ranges(lines[0]);
    let mut current_ranges = seed_ranges;

    let mut line_num = 1;
    while line_num < lines.len() {
        let line = lines[line_num];
        if line.contains("map") {
            println!("Processing map {}", line);
            let (end_line_num, new_ranges) =
                parse_and_map_ranges(&lines, line_num, &current_ranges);
            line_num = end_line_num;
            current_ranges = new_ranges;
        }
        line_num += 1;
    }
    // Get the range with the min start.
    println!(
        "Min final range is {:?}",
        current_ranges.iter().min_by_key(|r| r.start)
    );
}

#[derive(Clone, Copy, Debug)]
struct Range {
    start: i64,
    end: i64,
}

impl Range {
    fn new(start: i64, length: i64) -> Self {
        Range {
            start,
            end: start + length - 1,
        }
    }

    fn is_empty(&self) -> bool {
        self.start >= self.end
    }
}

#[derive(Debug)]
struct Mapping {
    src: Range,
    dst_start: i64,
}
impl Mapping {
    fn new(dst_start: i64, src_start: i64, length: i64) -> Self {
        Mapping {
            src: Range::new(src_start, length),
            dst_start,
        }
    }

    fn in_range(&self, value: i64) -> bool {
        value >= self.src.start && value <= self.src.end
    }

    fn can_map(&self, r: &Range) -> bool {
        self.in_range(r.start)
            || self.in_range(r.end)
            || (r.start < self.src.start && r.end > self.src.end)
    }

    fn map_value(&self, v: i64) -> i64 {
        self.dst_start + v - self.src.start
    }

    fn map_range(&self, r: &Range) -> (Range, Range, Range) {
        let mappable_start = self.src.start.max(r.start);
        let mappable_end = self.src.end.min(r.end);
        let new_range = Range {
            start: self.map_value(mappable_start),
            end: self.map_value(mappable_end),
        };
        // remainder 1 is the stuff before.
        let remainder1 = Range {
            start: r.start,
            end: mappable_start - 1,
        };
        // remainder 2 is the stuff after.
        let remainder2 = Range {
            start: mappable_end + 1,
            end: r.end,
        };

        (new_range, remainder1, remainder2)
    }
}

fn parse_seed_ranges(line: &str) -> Vec<Range> {
    let mut nums = vec![];
    for x in line.split(" ") {
        if let Ok(x) = x.parse::<i64>() {
            nums.push(x);
        }
    }
    let mut seed_ranges = vec![];
    for i in 0..nums.len() / 2 {
        seed_ranges.push(Range::new(nums[i * 2], nums[i * 2 + 1]));
    }
    seed_ranges
}

fn parse_and_map_ranges(
    lines: &Vec<&str>,
    line_num: usize,
    ranges: &Vec<Range>,
) -> (usize, Vec<Range>) {
    let mut mappings = vec![];
    let mut line_num = line_num + 1;
    loop {
        let line = lines[line_num];
        if line.is_empty() {
            break;
        }
        let nums = line.split(" ").collect::<Vec<_>>();
        let nums = nums
            .iter()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<_>>();
        mappings.push(Mapping::new(nums[0], nums[1], nums[2]));
        line_num += 1;
        if line_num >= lines.len() {
            break;
        }
    }

    // Strategy is to apply each mapping, and produce a remainder before/after, which could be empty ranges.
    let mut current_ranges = ranges.clone();
    let mut new_ranges = Vec::with_capacity(ranges.len());
    for mapping in mappings {
        let mut range_index = 0;
        while range_index < current_ranges.len() {
            let range = current_ranges[range_index];
            if mapping.can_map(&range) {
                let (new_range, remainder1, remainder2) = mapping.map_range(&range);
                new_ranges.push(new_range);
                // Always replace with a remainder 1 even if empty, just to avoid reshuffling.
                current_ranges[range_index] = remainder1;
                if !remainder2.is_empty() {
                    current_ranges.push(remainder2);
                }
            }
            range_index += 1;
        }
    }
    // Everything unmapped carries forward.
    for range in current_ranges {
        if !range.is_empty() {
            new_ranges.push(range);
        }
    }
    (line_num, new_ranges)
}
