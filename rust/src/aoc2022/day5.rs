use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;

pub fn day5(path: &String) {

    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();

    let mut crates9k = (0..9)
        .map(|i| {
            data[0..8]
                .iter()
                .map(|d| d.chars().nth(4 * i + 1).unwrap())
                .filter(|&d| d != ' ')
                .rev()
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let mut crates9k1 = crates9k.clone();

    let moves = data[10..]
        .iter()
        .map(|row| {
            let parts:Vec<&str> = row.split(" ").collect();
            (
                parts[1].parse::<usize>().unwrap(),
                parts[3].parse::<usize>().unwrap() - 1,
                parts[5].parse::<usize>().unwrap() - 1,
            )
        })
        .collect::<Vec<_>>();

    for m in moves {
        let (qty, src, dst) = m;

        let mut stack:Vec<char> = vec![]; 
	    let mut crates9k_dst = crates9k[dst].clone();
	    let mut crates9k1_dst = crates9k1[dst].clone();

	    for _ in 0..qty {
            stack.push(crates9k1[src].pop().unwrap());
	    }
	    for _ in 0..qty {
            crates9k_dst.push(crates9k[src].pop().unwrap());
		    crates9k1_dst.push(stack.pop().unwrap());
	    }
	    
	    crates9k[dst] = crates9k_dst;
	    crates9k1[dst] = crates9k1_dst;
    }

    println!("Part 1: {}", crates9k.iter().map(|c| c.last().unwrap()).collect::<String>());
    println!("Part 2: {}", crates9k1.iter().map(|c| c.last().unwrap()).collect::<String>());
}
