
// suppress style warnings
#![allow(non_snake_case)] // 'W'
#![allow(non_upper_case_globals)] // 'input'

use std::mem::{MaybeUninit};

const input: &str = "";

fn solution(str_s: &str) {
    let mut i: usize = 0;
    let W: usize = str_s.find('\n').unwrap() + 1;
    let s: &[u8] = str_s.as_bytes(); // for indexing

    let mut part1: u32 = 0;
    let mut part2: u32 = 0;

    // seems these both warn the same (work anyway)
    let mut nums: [u32; 20] = unsafe {std::mem::transmute::<_, [u32;20]>(MaybeUninit::<[u32;20]>::uninit().assume_init())};
    let mut gear_pos: [usize; 20] = unsafe {MaybeUninit::uninit().assume_init()};
    let mut start: usize = 0;
    let mut end: usize = 0;

    // parse all the numbers and sum the totals online
    while i < s.len() {
        if b'0'<=s[i] && s[i]<=b'9' {
            let mut j = i+1;
            while b'0' <= s[j] && s[j] <= b'9' { j += 1; }
            // check if symbol next to the number
            let mut has_symbol: bool = false;
            let mut gear_p: usize = 0;
            let tmp_range = -1..2;
            for y in tmp_range {
                for x in i-1..j+1 {
                    let np: i32 = y*(W as i32) + (x as i32);
                    if np < 0 || np > (s.len() as i32) {continue;}
                    let p: usize = np as usize;
                    if s[p] != b'.' && s[p]!=b'\n' && (s[p]<b'0' || s[p]>b'9') {
                        has_symbol = true;
                        if s[p]==b'*' {gear_p = p;}
                    }
                }
            }
            if has_symbol {
                let n: u32 = std::str::from_utf8(&s[i..j]).unwrap().parse::<u32>().unwrap();
                part1 += n;
                if gear_p != 0 {
                    // small resident set size makes linear search in a circular buffer fast enough
                    // although maybe not as terse as a hashmap
                    let mut found = false;
                    for stored in start..end { // search in DB
                        if gear_pos[stored%20]==gear_p { // next to the same gear (assume only 2 nums can be)
                            part2 += nums[stored%20] * n;
                            if stored == start {start += 1;} // remove (consume)
                            found = true;
                            break;
                        } else if (i > 2*W) && (gear_pos[stored%20] < i - W) && start==stored {
                            start += 1; // remove (can no longer be matched)
                        }
                    }
                    if !found { // insert to DB
                        gear_pos[end%20] = gear_p;
                        nums[end%20] = n;
                        end += 1;
                    }
                }
            } //has_symbol
            i = j;
        } // finished parsing a number s[i..j]
        i += 1;
    }
    println!("{}\n{}\n", part1, part2);
}

fn main() {
    solution(input);
}