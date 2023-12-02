use std::env;
use std::fs;

pub fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let filename = args.get(1).expect("Provide an input filename.");

    fs::read_to_string(filename).expect("Should have been able to read the file")
}
