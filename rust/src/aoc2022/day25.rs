use num::checked_pow;
use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;


pub fn day25(path: &String) {
    println!("Day 25");
    let rounds:Vec<String> = File::open(path).read_lines::<String>(1).collect();
    
    println!("Part 1: {}", dec_to_bquint(rounds.iter().map(|v| bquint_to_dec(&v)).sum::<i64>()));

}

fn bquint_to_dec(value: &String) -> i64 {
    let n:i64 = value.chars().rev().enumerate().map(|(i, c)| {
        match c {
            '=' => -2 * checked_pow(5, i).unwrap(),
            '-' => -1 * checked_pow(5, i).unwrap(),
            '0' => 0,
            '1' => 1 * checked_pow(5, i).unwrap(),
            _ => 2 * checked_pow(5, i).unwrap()
        }
    }).sum();
    return n;
}

fn dec_to_bquint(value: i64) -> String {
    let mut base_num:Vec<i64> = Vec::new();
    let mut val = value;

    // Convert to base 5
    while val > 0 {
        let dig = val % 5;
        base_num.push(dig);
        val = (val - dig) / 5;
    }
    // Carry forward
    let mut balanced_base_num = "".to_string();
    let mut carry = 0;
    for d in base_num{
        let  k = d + carry;
        carry = 1;
        match k {
            0 => {carry = 0; balanced_base_num.push('0')},
            1 => {carry = 0; balanced_base_num.push('1')},
            2 => {carry = 0; balanced_base_num.push('2')},
            3 => {balanced_base_num.push('=')},
            4 => {balanced_base_num.push('-')},
            _ => {balanced_base_num.push('0')},
        }
    }
    if carry == 1 {
        balanced_base_num.push('1');
    }
    balanced_base_num = balanced_base_num.chars().rev().collect();
    return balanced_base_num;
}
