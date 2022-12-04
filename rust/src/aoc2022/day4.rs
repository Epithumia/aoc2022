use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;

pub fn day4(path: &String) {
    println!("Day 4");
    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();
    let mut nb_elves_over:u32 = 0;
    let mut nb_elves_inter = 0;
    for row in data{
        let pair:Vec<u32> = row.split(&['-', ','][..]).map(|s| s.parse::<u32>().unwrap()).collect();
        let res = overwork(pair[0], pair[1], pair[2], pair[3]);
        nb_elves_over += res[0];
        nb_elves_inter += res[1];
    }
    
    println!("Part 1: {}", nb_elves_over);
    println!("Part 2: {}", nb_elves_inter);
}

fn overwork(n1:u32, n2: u32, m1: u32, m2: u32) -> Vec<u32> {
    let mut full = 0;
    let mut partial = 0;
    if ((n1 <= m1 && m1 <= n2) && (n1 <= m2 && m2 <= n2)) || ((m1 <= n1 && n1 <= m2) && (m1 <= n2 && n2 <= m2)){
        full = 1;
    }
    if ((n1 <= m1 && m1 <= n2) || (n1 <= m2 && m2 <= n2)) || ((m1 <= n1 && n1 <= m2) || (m1 <= n2 && n2 <= m2)){
        partial = 1;
    }
    return vec![full, partial]
}