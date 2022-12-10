use num::{abs, signum};
use rdcl_aoc_helpers::input::WithReadLines;
use std::{fs::File, collections::HashSet};

pub fn day9(path: &String) {
    println!("Day 9");
    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();
    println!("Part 1: {}", rope(data.clone(), 2));
    println!("Part 2: {}", rope(data, 10));
}

fn rope(moves: Vec<String>, length:usize) -> u32 {
    let mut pos = vec![vec![0; 2]; length];
    let mut visited: HashSet<Vec<i32>> = HashSet::new();
    visited.insert(pos[length - 1].clone());
    for movement in moves {
        let step:Vec<String> = movement.split(' ').into_iter().map(|x| x.to_string()).collect();
        let dir = step[0].clone();
        let dist:usize = step[1].parse::<usize>().unwrap();
        for _ in 0..dist {
            match dir.as_str() {
                "U" => {
                    pos[0][1] += 1;
                },
                "D" => {
                    pos[0][1] += -1;
                },
                "R" => {
                    pos[0][0] += 1;
                },
                "L" => {
                    pos[0][0] -= 1;
                },
                _ => println!("Error"),
            }
            for i in 1..length {
                pos[i] = follow(pos[i-1].clone(), pos[i].clone());
            }
            visited.insert(pos[length-1].clone());
        }
    }
    return visited.len() as u32;
}

fn follow(pos_h: Vec<i32>, pos_t:Vec<i32>) -> Vec<i32> {
    let mut pos = pos_t.clone();
    let dx = abs(pos_h[0] - pos_t[0]);
    let dy = abs(pos_h[1] - pos_t[1]);
    let vx = signum(pos_h[0] - pos_t[0]) * ((((dx >= 1) && (dy > 1)) || (dx > 1)) as i32);
    let vy = signum(pos_h[1] - pos_t[1]) * ((((dx > 1) && (dy >= 1)) || (dy > 1)) as i32);
    pos[0] += vx;
    pos[1] += vy;
    return pos
}