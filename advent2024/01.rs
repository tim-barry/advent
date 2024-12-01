
// Paste in input for rust online playground
const input: &str = include_bytes!("input01.txt");

fn main() {
    let mut part1: i32 = 0;
    let mut part2: i32 = 0;

    let mut left: Vec<i32> = Vec::with_capacity(1000);
    let mut right: Vec<i32> = Vec::with_capacity(1000);

    for line in input.lines() {
        if line.len()==0 {continue;}

        let l = line[0..5].parse::<i32>().unwrap();
        let r = line[8..13].parse::<i32>().unwrap();
        left.push(l);
        right.push(r);
    }
    // part 1
    left.sort();
    right.sort();
    for pair in left.iter().zip(right.iter()) {
        let (l, r) = pair;
        part1 += (l - r).abs();
    }
    // part 2
    for l in left.iter() {
        part2 += l * right.iter().filter(|x| *x==l).count() as i32;
    }
    print!("{part1}\n{part2}\n", part1=part1, part2=part2);
}
