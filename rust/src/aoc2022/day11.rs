use rdcl_aoc_helpers::input::WithReadLines;
use std::{fs::File, collections::VecDeque};

pub fn day11(path: &String) {
    println!("Day 11");
    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();

    let mut monkeys: MonkeyCircus = MonkeyCircus(Vec::new());
    for i in 0..((data.len()+1)/7 as usize) {
        monkeys.push(Monkey::new(data[7*i..(7*i+6)].to_vec()));
    }

    for _ in 0..20 {
        for i in 0..monkeys.0.len() {
            let nb_items = monkeys.0[i].items.len();
            for _ in 0..nb_items {
                let mut monkey = monkeys.0[i].clone();
                monkey.inspect();
                monkey.get_bored(0);
                let t = monkey.pass_to();
                let item = monkey.pass_item();
                monkeys.0[i] = monkey.clone();
                let mut friend = monkeys.0[t as usize].clone();
                friend.receive_item(item);
                monkeys.0[t as usize] = friend;
            }
        }
    }

    let mut monkey_business:Vec<u64> = monkeys.0.iter().map(|x| x.activity).collect();
    monkey_business.sort();
    monkey_business.reverse();
    println!("Part 1: {}", monkey_business[0] * monkey_business[1]);

    monkeys.0.clear();
    let mut worry = 1;

    for i in 0..((data.len()+1)/7 as usize) {
        let m = Monkey::new(data[7*i..(7*i+6)].to_vec());
        monkeys.push(m.clone());
        worry = worry * m.test;
    }

    for _ in 0..10000 {
        for i in 0..monkeys.0.len() {
            let nb_items = monkeys.0[i].items.len();
            for _ in 0..nb_items {
                let mut monkey = monkeys.0[i].clone();
                monkey.inspect();
                monkey.get_bored(worry);
                let t = monkey.pass_to();
                let item = monkey.pass_item();
                monkeys.0[i] = monkey.clone();
                let mut friend = monkeys.0[t as usize].clone();
                friend.receive_item(item);
                monkeys.0[t as usize] = friend;
            }
        }
    }

    monkey_business = monkeys.0.iter().map(|x| x.activity).collect();
    monkey_business.sort();
    monkey_business.reverse();
    println!("Part 2: {}", monkey_business[0] * monkey_business[1]);

}

#[derive(Debug)]
struct MonkeyCircus(Vec<Monkey>);

impl MonkeyCircus {
    fn push(&mut self, monkey: Monkey) {
        self.0.push(monkey);
    }    
}

#[derive(Debug, Clone)]
struct Monkey {
    items: VecDeque<u64>,
    oper: char,
    val: String,
    test: u64,
    t: u8,
    f:u8,
    activity: u64,
}

impl Monkey {
    fn new(data : Vec<String>) -> Monkey {
        let oper = data.iter().nth(2).unwrap().split("new = old ").last().unwrap().chars().nth(0).unwrap();
        let val = data.iter().nth(2).unwrap().split("new = old ").last().unwrap().split(' ').last().unwrap().to_string();
        let test =  data.iter().nth(3).unwrap().split("by ").last().unwrap().parse::<u64>().unwrap();
        let t =  data.iter().nth(4).unwrap().split("monkey ").last().unwrap().parse::<u8>().unwrap();
        let f =  data.iter().nth(5).unwrap().split("monkey ").last().unwrap().parse::<u8>().unwrap();
        let mut items:VecDeque<u64> = VecDeque::new();
        for item in data.iter().nth(1).unwrap().split(": ").last().unwrap().split(", "){
           items.push_back(item.parse::<u64>().unwrap());
        }
        Monkey { 
            items, 
            oper,
            val,
            test, 
            t, 
            f, 
            activity: 0 
        }
    }

    fn inspect(&mut self) {
        self.activity += 1;
        let val;
        if self.val == "old" {
            val = self.items[0];
        } else {
            val = self.val.parse::<u64>().unwrap();
        }
        if self.oper == '+' {
            self.items[0] = self.items[0] + val;
        } else {
            self.items[0] = self.items[0] * val;
        }
    }

    fn get_bored(& mut self, worry: u64) {
        if worry == 0{
            self.items[0] = self.items[0] / 3;
        }else{
            self.items[0] = self.items[0] % worry;
        }
    }

    fn pass_to(&self) -> u8 {
        if self.items[0] % self.test == 0{
            return self.t;
        }
        return self.f;
    }

    fn pass_item(&mut self) -> u64 {
        return self.items.pop_front().unwrap();
    }

    fn receive_item(&mut self, item:u64) {
        self.items.push_back(item);
    }
}