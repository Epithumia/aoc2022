use rdcl_aoc_helpers::input::WithReadMultiLines;
use rdcl_aoc_helpers::error::{ParseError};
use rdcl_aoc_helpers::input::MultilineFromStr;
use std::fs::File;


pub fn day1(path: &String) {
    println!("Day 1");
    let meals:Vec<Record> = File::open(path).read_multi_lines::<Record>(1).collect();
    let mut packed_meals:Vec<u32> = meals.iter().map(|m| m.weight()).collect();
    packed_meals.sort();
    packed_meals.reverse();
    
    println!("Part 1: {}", packed_meals[0]);
    println!("Part 2: {}", packed_meals.iter().take(3).sum::<u32>());
    //println!("{:?}", packed_meals);
    
}
#[derive(Debug)]
pub struct Record {
    items: Vec<u32>,   
}

impl Record {
    fn weight(&self) -> u32 {
        return self.items.iter().sum();
    }
}

impl MultilineFromStr for Record {
    type Err = ParseError;

    fn new() -> Self {
        Record {
            items: Vec::new(),
        }
    }

    fn indicates_new_record(&self, line: &str) -> bool {
        line.is_empty()
    }

    fn parse(&mut self, line: &str) -> Result<(), Self::Err> {
        if !line.is_empty() {
            self.items.push(line.parse::<u32>()?);
        }

        Ok(())
    }
}