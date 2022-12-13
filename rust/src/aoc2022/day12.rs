use rdcl_aoc_helpers::{input::WithReadLines};
use std::{fs::File, collections::{HashMap, BinaryHeap}, cmp::Ordering};

pub fn day12(path: &String) {
    println!("Day 12");
    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();
    let jungle_map = JungleMap::new(data);
    println!("Part 1: {}", jungle_map.clone().explore("reach".to_string()));
    println!("Part 2: {}", jungle_map.explore("hike".to_string()));

}

#[derive(Debug, Clone)]
struct JungleMap {
    candidates: Vec<(usize, usize)>,
    adj: HashMap<(usize, usize), Vec<(usize, usize)>>,
    start: (usize, usize),
    end: (usize, usize)
}

impl JungleMap {
    fn new(data: Vec<String>) -> JungleMap {
        let mut start = (0, 0);
        let mut end = (0, 0);
        let mut i = 0;
        let mut candidates: Vec<(usize, usize)> = Vec::new();
        let mut dmap: Vec<Vec<char>> = Vec::new();
        let mut adj: HashMap<(usize, usize), Vec<(usize, usize)>> = HashMap::new();
        for row in data {
            let mut drow: Vec<char> = Vec::new();
            let mut j = 0;
            for mut p in row.chars() {
                if p == 'S' {
                    p = 'a';
                    start = (i, j);
                }
                if p == 'E' {
                    p = 'z';
                    end = (i, j);
                }
                if p == 'a' {
                    candidates.push((i,j));
                }
                drow.push(p);
                j += 1;
            }
            dmap.push(drow);
            i += 1;
        }
        for i in 0..(dmap.len()) {
            for j in 0..(dmap[0].len()) {
                adj.insert((i, j), get_neighbors(i, j, &dmap));
            }
        }
        JungleMap { 
            candidates, 
            adj, 
            start, 
            end
        }
    }

    fn explore(self, mode: String) -> usize{
        if mode == "reach" {
            let cost = self.dijkstra(self.start).unwrap();
            return cost;
        } else {
            let mut min_cost:usize = usize::MAX;
            for point in self.candidates.iter() {
                let cost = self.dijkstra(point.clone()).unwrap();
                if cost < min_cost {
                    min_cost = cost;
                }
            }
            return min_cost;
        }
    }

    fn dijkstra(&self, point: (usize, usize)) -> Option<usize> {
        let mut heap:BinaryHeap<State> = BinaryHeap::new();
        let mut dist:HashMap<(usize, usize), usize> = HashMap::new();
        heap.push(State { cost: 0, position: point });
        dist.insert(point, 0);

        while let Some(State { cost, position }) = heap.pop() {
            if position == self.end { return Some(cost); }
            if cost > *dist.get(&position).unwrap() { continue; }
            for neighbour in self.adj.get(&position).unwrap() {
                let next = State{ cost: cost + 1, position: *neighbour };
                if next.cost < *dist.get(&next.position).unwrap_or(&usize::MAX) {
                    heap.push(next);
                    dist.insert(next.position, next.cost);
                }
            }
        }
        Some(usize::MAX)
    }
    
}

fn get_neighbors(i: usize, j:usize, dmap: &Vec<Vec<char>>) -> Vec<(usize, usize)> {
    let mut neighbours: Vec<(usize, usize)> = Vec::new();
    if i > 0 && dmap[i-1][j] as u32 - 1 <= dmap[i][j] as u32 {
        neighbours.push((i-1, j));
    }
    if j > 0 && dmap[i][j-1] as u32 - 1 <= dmap[i][j] as u32 {
        neighbours.push((i, j-1));
    }
    if i < dmap.len() - 1 && dmap[i+1][j] as u32 - 1 <= dmap[i][j] as u32 {
        neighbours.push((i+1, j));
    }
    if j < dmap[0].len() - 1 && dmap[i][j+1] as u32 - 1 <= dmap[i][j] as u32 {
        neighbours.push((i, j+1));
    }
    neighbours
}

// The State struct and basic Dijkstra implemntation comes from the Rust doc.
#[derive(Copy, Clone, Eq, PartialEq, Debug)]
struct State {
    cost: usize,
    position: (usize, usize),
}

// The priority queue depends on `Ord`.
// Explicitly implement the trait so the queue becomes a min-heap
// instead of a max-heap.
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // Notice that the we flip the ordering on costs.
        // In case of a tie we compare positions - this step is necessary
        // to make implementations of `PartialEq` and `Ord` consistent.
        other.cost.cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

// `PartialOrd` needs to be implemented as well.
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}