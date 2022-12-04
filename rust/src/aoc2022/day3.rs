use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;
use array_tool::vec::Intersect;


pub fn day3(path: &String) {
    println!("Day 3");
    let bags:Vec<String> = File::open(path).read_lines::<String>(1).collect();
    let mut score1:u32 = 0;
    let mut score2 = 0;

    let rebag:Vec<Vec<u8>> = bags.iter().map(|x| x.chars().into_iter().map(|c| elfebet(c)).collect()).collect();

    for bag in rebag.clone() {
        let (aleft, aright) = bag.split_at(bag.len() / 2);
        let left = aleft.to_vec();
        let right = aright.to_vec();
        let el = left.intersect(right);
        score1 += el[0] as u32;
    }

    for i in 0..rebag.len()/3 {
        let bag1 = rebag[3*i].clone();
        let bag2 = rebag[3*i+1].clone();
        let bag3 = rebag[3*i+2].clone();
        let t = bag1.intersect(bag2).intersect(bag3);
        score2 += t[0] as u32;
    }
    
    println!("Part 1: {}", score1);
    println!("Part 2: {}", score2);
}

fn elfebet(c: char) -> u8 {
    if c <= 'z' && c>= 'a' {
        return (c as u8) - ('a' as u8) + 1;
    }
    if c <= 'Z' && c>= 'A' {
        return (c as u8) - ('A' as u8) + 27;
    }
    return 0;
}