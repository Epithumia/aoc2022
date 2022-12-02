use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;


pub fn day2(path: &String) {
    println!("Day 2");
    let rounds:Vec<String> = File::open(path).read_lines::<String>(1).collect();
    let mut score1 = 0;
    let mut score2 = 0;

    for round in rounds {
        score1 += score(&round);
        score2 += strategize(&round);
    }
    
    println!("Part 1: {}", score1);
    println!("Part 2: {}", score2);
}

fn map(m: char) -> usize {
    match m{
        'A' => return 0,
        'B' => return 1,
        'C' => return 2,
        'X' => return 0,
        'Y' => return 1,
        'Z' => return 2,
        _ => return 0
    }
}

fn score(s: &str) -> u32 {
    let scores = vec![
        vec![1+3, 2+6, 3+0],
        vec![1+0, 2+3, 3+6],
        vec![1+6, 2+0, 3+3]
        ];
    let p1:usize = map(s.chars().nth(0).unwrap());
    let p2:usize = map(s.chars().nth(2).unwrap());
    return scores[p1][p2];
    //return 0;
}
fn strategize(s: &str) -> u32 {
    let scores = vec![
        vec![3+0, 1+3, 2+6],
        vec![1+0, 2+3, 3+6],
        vec![2+0, 3+3, 1+6]
        ];
        let p1:usize = map(s.chars().nth(0).unwrap());
        let p2:usize = map(s.chars().nth(2).unwrap());
        return scores[p1][p2];
        //return 0;
}