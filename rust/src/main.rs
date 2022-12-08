mod aoc2022;

use crate::aoc2022::day1::day1;
use crate::aoc2022::day2::day2;
use crate::aoc2022::day3::day3;
use crate::aoc2022::day4::day4;
use crate::aoc2022::day5::day5;
use crate::aoc2022::day6::day6;
/*use crate::aoc2022::day7::day7; Not working */
use crate::aoc2022::day8::day8;
/*use crate::aoc2022::day9::day9;
use crate::aoc2022::day10::day10;
use crate::aoc2022::day11::day11;
use crate::aoc2022::day12::day12;
use crate::aoc2022::day13::day13;
use crate::aoc2022::day14::day14;
use crate::aoc2022::day15::day15;
use crate::aoc2022::day16::day16;
use crate::aoc2022::day17::day17;
use crate::aoc2022::day19::day19;
use crate::aoc2022::day20::day20;
use crate::aoc2022::day21::day21;
use crate::aoc2022::day22::day22;
use crate::aoc2022::day23::day23;
use crate::aoc2022::day24::day24;
use crate::aoc2022::day25::day25;
*/
use rdcl_aoc_helpers::args::get_args;

fn main() {
    let args = get_args(&["<day>", "<inputs path>"], 1);
    let day: u8 = args[1].parse::<u8>().unwrap();
    let path = &args[2];

    match day {
        1 => day1(&path.to_string()),
        2 => day2(&path.to_string()),
        3 => day3(&path.to_string()),
        4 => day4(&path.to_string()),
        5 => day5(&path.to_string()),
        6 => day6(&path.to_string()),
        // 7 => day7(&path.to_string()), // Not working
        8 => day8(&path.to_string()),
        /*9 => day9(&path.to_string()),
        10 => day10(&path.to_string()),
        11 => day11(&path.to_string()),
        12 => day12(&path.to_string()),
        13 => day13(&path.to_string()),
        14 => day14(&path.to_string()),
        15 => day15(&path.to_string()),
        16 => day16(&path.to_string()),
        17 => day17(&path.to_string()),
        19 => day19(&path.to_string()),
        20 => day20(&path.to_string()),
        21 => day21(&path.to_string()),
        22 => day22(&path.to_string()),
        23 => day23(&path.to_string()),
        24 => day24(&path.to_string()),
        25 => day25(&path.to_string()),*/
        _ => println!("Nothing to do"),
        // Jour non codé
    }
}
