
use std::collections::HashSet;
use std::str::FromStr;

const input: &str = include_str!("input04.txt");

fn main() {
    let mut set = HashSet::with_capacity(10);
    // part2 'lookahead' up to 10 (max number of matches)
    let mut next_card_counts: [u32;10] = [1;10];
    let mut card_i: u8 = 0;

    let mut part1: u32 = 0;
    let mut part2: u32 = 0;
    for line in input.lines() {
        // parse line and count matches
        let mut matches: u8 = 0; // <=10
        let mut num_it = line.split_ascii_whitespace();
        num_it.next(); num_it.next();
        for chunk in num_it.by_ref() {
            if chunk.chars().nth(0)==Some('|') {break;}
            let n = u8::from_str(chunk).unwrap();
            set.insert(n);
        }
        for chunk in num_it {
            let n = u8::from_str(chunk).unwrap();
            if set.contains(&n) {
                matches += 1;
            }
        }
        // now have matches
        if matches > 0 {
            part1 += 1u32<<(matches-1);
        }
        // get count of this card for part2
        let this_card_count = next_card_counts[(card_i%10) as usize];
        next_card_counts[(card_i%10) as usize] = 1;
        part2 += this_card_count;
        for won_card in 1..matches+1 {
            next_card_counts[((card_i + won_card)%10) as usize] += this_card_count;
        }
        card_i += 1;
        set.drain();
    }
    println!("part1: {}\npart2: {}\n", part1, part2);
}

