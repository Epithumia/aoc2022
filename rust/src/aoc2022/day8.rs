use rdcl_aoc_helpers::input::WithReadLines;
use std::{fs::File};

pub fn day8(path: &String) {

    let data:Vec<String> = File::open(path).read_lines::<String>(1).collect();

    let treemap: Vec<Vec<u32>> = data.iter().map(|row| row.chars().map(|c| c.to_digit(10).unwrap()).collect()).collect();

    let height = treemap.len();
    let width = treemap[0].len();

    let mut visiblemap = treemap.clone();
    visiblemap.iter_mut().for_each(|row| row.iter_mut().for_each(|c| *c = 0));

    for i in 0..height {
        for j in 0..width {
            if i == 0 || j == 0 || i == height-1 || j == width-1 {
                visiblemap[i][j] = 1;
            }
        }
    }

    for i in 1..height-1 {
        let mut curmaxl:u32 = 0;
        let mut curmaxr:u32 = 0;
        for j in 1..width-1 {
            if treemap[i][j - 1] > curmaxl{
                curmaxl = treemap[i][j - 1];
            }
            if curmaxl < treemap[i][j]{
                visiblemap[i][j] = 1;
            }
            if treemap[(height - 1) - i][(width - 1) - (j - 1)] > curmaxr {
                curmaxr = treemap[(height - 1) - i][(width - 1) - (j - 1)];
            }
                
            if curmaxr < treemap[(height - 1) - i][(width - 1) - j]{
                visiblemap[(height - 1) - i][(width - 1) - j] = 1;
            }
        }
    }

    for j in 1..width-1 {
        let mut curmaxl:u32 = 0;
        let mut curmaxr:u32 = 0;
        for i in 1..height-1 {
            if treemap[i - 1][j] > curmaxl{
                curmaxl = treemap[i - 1][j];
            }
            if curmaxl < treemap[i][j]{
                visiblemap[i][j] = 1;
            }
            if treemap[(height - 1) - (i - 1)][(width - 1) - j] > curmaxr {
                curmaxr = treemap[(height - 1) - (i - 1)][(width - 1) - j];
            }
                
            if curmaxr < treemap[(height - 1) - i][(width - 1) - j]{
                visiblemap[(height - 1) - i][(width - 1) - j] = 1;
            }
        }
    }

    let mut best:u32 = 0;
    let mut score:u32;
    for i in 1..height-1{
        for j in 1..width-1{
            score = view(i, j, &treemap);
            if score > best{
                best = score;
            }
        }
    }

    println!("Part 1: {}", visiblemap.iter().map(|x| -> u32 { x.iter().sum() }).sum::<u32>());
    println!("Part 2: {}", best);
}

fn view(i:usize, j:usize, treemap:&Vec<Vec<u32>>) -> u32 {
    let mut scorerl:u32 = 0;
    let mut scorerr:u32 = 0;
    let mut scorecl:u32 = 0;
    let mut scorecr:u32 = 0;
    for r in 1..(i+1) {
        if treemap[i - r][j] < treemap[i][j]{
            scorerl += 1;
        } else {
            scorerl += 1;
            break
        }
    }
    for r in 1..(treemap.len() - i){
        if treemap[i + r][j] < treemap[i][j]{
            scorerr += 1;
        }
        else{
            scorerr += 1;
            break
        }
    }
    for c in 1..(j+1) {
        if treemap[i][j - c] < treemap[i][j] {
            scorecl += 1;
        } else {
            scorecl += 1;
            break;
        }
    }
    for c in 1..(treemap.len() - j) {
        if treemap[i][j + c] < treemap[i][j] {
            scorecr += 1;
        } else {
            scorecr += 1;
            break;
        }
    }


    let score = scorecl * scorecr * scorerl * scorerr;
    score
}