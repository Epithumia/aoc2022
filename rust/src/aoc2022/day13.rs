use rdcl_aoc_helpers::input::WithReadLines;
use std::cmp::Ordering::{*, self};
use std::fs::File;
use serde::Deserialize;

pub fn day13(path: &String) {
    println!("Day 13");
    let mut packets:Vec<Packet> = File::open(path).read_lines::<String>(1).filter(|s| s.len() > 0).map(|l| {let p:Packet = serde_json::from_str(&l.to_string()).unwrap(); return p;}).collect();
    let mut score1 = 0;
    let mut i = 1;

    for packet in packets.chunks(2) {
        if packet[0].clone() > packet[1].clone() {
            score1 += i;
        }
        i += 1;
    }

    println!("Part 1: {}", score1);

    packets.push(serde_json::from_str("[[2]]").unwrap());
    packets.push(serde_json::from_str("[[6]]").unwrap());
    packets.sort_by(|a, b| b.cmp(a));

    let mut score2 = 1;
    for i in 0..packets.len() {
        if packets[i] == serde_json::from_str("[[2]]").unwrap() || packets[i] == serde_json::from_str("[[6]]").unwrap() {
            score2 *= i+1;
        }
    }

    println!("Part 2: {}", score2);
    
}

#[derive(Debug, Deserialize, Clone, PartialEq, Eq)]
#[serde(untagged)]
enum Packet {
    P(Vec<Packet>),
    V(u8),
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Packet::V(l), Packet::V(r)) => {
                return r.cmp(l);
            }
            (Packet::V(l), Packet::P(_)) => {
                let p:Packet = Packet::P(vec![Packet::V(*l)]);
                return p.cmp(other);
            }
            (Packet::P(_), Packet::V(r)) => {
                let p:Packet = Packet::P(vec![Packet::V(*r)]);
                return self.cmp(&p);
            }
            (Packet::P(l), Packet::P(r)) => {
                if l.len() == 0 && r.len() > 0 {return Greater;}
                if r.len() == 0 && l.len() > 0 {return Less;}
                if l.len() == 0 && r.len() == 0 {return Equal;}
                let res = l[0].cmp(&r[0]);
                if res != Equal {return res;}
                let lc = Packet::P(l.clone()[1..].to_vec());
                let rc = Packet::P(r.clone()[1..].to_vec());
                return lc.cmp(&rc);
            }
        }
    }
}

impl PartialOrd for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}