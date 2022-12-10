use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;

pub fn day10(path: &String) {
    println!("Day 10");
    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();

    let mut x:Vec<i32> = vec![1, 1];

    for instr in data{
        if instr.chars().nth(0).unwrap() == 'n' {
            x.push(*x.last().unwrap());
        } else {
            let val:i32 = instr.split(' ').nth(1).unwrap().parse::<i32>().unwrap();
            x.push(*x.last().unwrap());
            x.push(*x.last().unwrap() + val);
        }
    }
    println!("Part 1: {}", (20..221).step_by(40).map(|i| (i as i32)*x[i]).sum::<i32>());

    let mut s = String::new();
    for row in 0..6 {
        s += "\n";
        let mut pos = 0;
        for cycle in (40*row+1)..(40*(row+1)+1) {
            let sprite = x[cycle];
            if sprite - 1 <= pos && pos <= sprite + 1 {
                s+="#";
            } else {
                s+=".";
            }
            pos += 1;
        }
    }
    println!("Part 2: {}", s);
}