
use std::cmp::{max,min};
use itertools::Itertools;

const INPUT: &str = include_str!("input05.txt");

struct Seed {
    s: i64,
    moved: bool,
}
struct Range {
    i: i64,
    j: i64,
    moved: bool,
}

fn main() {
    let mut maps = INPUT.split("\n\n");
    let seedstr = maps.next().unwrap();
    let iseeds: Vec<i64> = seedstr.split(' ').skip(1).map(|x| x.parse::<i64>().unwrap()).collect();
    let mut ranges: Vec<Range> = iseeds.iter().tuples().map(|(s,len)| Range{i: *s, j: *s+*len, moved: false}).collect();
    let mut seeds: Vec<Seed> = iseeds.into_iter().map(|x| Seed{s: x, moved: false}).collect();
    // move the ranges and original seeds according to maps
    for map in maps {
        for map_part in map.lines().skip(1) {
            let (dst, src, len) = map_part.split(' ').map(|x| x.parse::<i64>().unwrap()).next_tuple().unwrap();
            let end = src + len;
            // move seeds according to map part
            for seed in &mut seeds {
                if seed.moved {continue;}
                if src <= seed.s && seed.s < end {
                    seed.s += dst-src;
                    seed.moved = true;
                }
            }
            for i in 0..ranges.len() {
                // intersect all ranges with the map part
                //let r = &ranges[i];
                if ranges[i].moved {continue;}
                let (ri, rj) = (ranges[i].i, ranges[i].j);
                if src < rj && ri < end {
                    let new_i = max(ri, src);
                    let new_j = min(rj, end);
                    if ri < new_i {
                        ranges.push(Range {i: ri, j: new_i, moved: false});
                    }
                    if new_j < rj {
                        ranges.push(Range {i: new_j, j: rj, moved: false});
                    }
                    ranges[i] = Range {i: new_i - src+dst, j: new_j - src+dst, moved: true};
                }
            }
        }
        // finished with this section; collect moved ranges
        for seed in &mut seeds {
            seed.moved = false;
        }
        for range in &mut ranges {
            range.moved = false;
        }
    }
    let part1 = seeds.into_iter().map(|x| x.s).min().unwrap();
    let part2 = ranges.into_iter().map(|x| x.i).min().unwrap();
    println!("part1: {}\npart2: {}\n", part1, part2);
}
