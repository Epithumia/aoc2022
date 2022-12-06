use rdcl_aoc_helpers::input::WithReadLines;
use std::{fs::File, collections::HashSet};

pub fn day6(path: &String) {

    let data:String = File::open(path).read_lines::<String>(1).collect();

    println!("Part 1: {}", tune(&data, 4).unwrap());
    println!("Part 2: {}", tune(&data, 14).unwrap());
}

fn tune(signal: &str, length: usize) -> Option<usize> {
    for i in 0..(signal.len() - length + 1) {
        let d = &signal[i..(i + length)];
        let s: HashSet<char> = d.chars().collect();
        if s.len() == length {
            return Some(i + length);
        }
    }
    None
}