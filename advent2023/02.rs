
// Based on 02.zig solution
use std::cmp::max;

struct Bag {
    red: u8,
    green: u8,
    blue: u8,
}
impl Bag {
    fn union_with(self: &mut Self, other: &Self) {
        self.red = max(self.red, other.red);
        self.green = max(self.green, other.green);
        self.blue = max(self.blue, other.blue);
    }
    fn contains(self: &Self, other: &Self) -> bool {
        return (self.red >= other.red) && (self.green >= other.green) && (self.blue >= other.blue);
    }
    fn power(self: &Self) -> u32 {
        return (self.red as u32) * (self.green as u32) * (self.blue as u32);
    }

}

const goal_bag: Bag = Bag{red: 12, green: 13, blue: 14};

// Paste in input for rust online playground
const input: &str = include_bytes!("input02.txt");

struct Game {
    id: u8,
    pulls: Vec<Bag>,
}
impl Game {
    fn id_if_possible(self: &Self) -> u8 {
        for pull in self.pulls.iter() {
            if !goal_bag.contains(pull) {return 0;}
        }
        return self.id;
    }
    fn min_bag(self: &Self) -> Bag {
        let mut bag = Bag{red: 0, green:0, blue:0};
        for pull in self.pulls.iter() {
            bag.union_with(pull);
        }
        return bag;
    }
}

fn main() {
    let mut part1: u32 = 0;
    let mut part2: u32 = 0;

    for line in input.lines() {
        //if line.len()==0 {continue;}
        let mut colon_it = line.split(':');
        let game_id = colon_it.next().unwrap();
        let rest_of_line = colon_it.next().unwrap();
        let mut game = Game{id: game_id[5..].parse::<u8>().unwrap(), pulls: vec![]};

        let pulls = rest_of_line.split(';');
        for pull in pulls {
            let mut p = Bag{red: 0, green: 0, blue: 0};
            let cubes = pull.split(',');
            for cube in cubes {
                let mut cube_it = cube[1..].split(' ');
                let n: u8 = cube_it.next().unwrap().parse::<u8>().unwrap();
                let s = cube_it.next().unwrap();
                match s {
                    "red" => p.red = n,
                    "green" => p.green = n,
                    "blue" => p.blue = n,
                    _ => (),
                }
            }
            game.pulls.push(p);
        }
        part1 += game.id_if_possible() as u32;
        part2 += game.min_bag().power();
    }
    print!("{part1}\n{part2}\n", part1=part1, part2=part2);
}
