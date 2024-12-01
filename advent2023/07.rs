
//use std::mem::MaybeUninit;
const input: &str = include_str!("input07.txt");

struct Hand {
    hand_type1: u8,
    hand_type2: u8,
    card_order: [u8; 5],
    bid: u32,
}

fn main() {
    let mut all_hands: Vec<Hand> = vec![];
    // read input
    for line in input.lines() {
        if line.len()==0 {continue;}
        //
        let hand_s = &line[0..5];
        let bid: u32 = line[6..].parse().unwrap();
        let mut card_order = [0u8;5];
        let mut counts = [0u8; 15]; // count of each card
        let mut ccounts: [u8;6] = [13, 0, 0, 0, 0, 0]; // most_common structure
        // generate card order (lexicographical ordering)
        for (ci, c) in hand_s.chars().enumerate() {
            let value: u8 = match c {
                '2'..='9' => (c as u8) - b'1', // 1...8
                'A' => 13,
                'K' => 12,
                'Q' => 11,
                'J' => 10,
                'T' => 9,
                _ => unreachable!(),
            };
            card_order[ci] = value;
            ccounts[counts[value as usize] as usize] -= 1;
            counts[value as usize] += 1;
            ccounts[counts[value as usize] as usize] += 1;
        }
        let hand_type1 = ccounts[5]*10 + ccounts[4]*9 + ccounts[3]*5 + ccounts[2];
        // hand_type2
        let jokers = counts[10];
        if 0 < jokers && jokers < 5 {
            ccounts[jokers as usize] -= 1;
            let mut ct: u8 = 4;
            // we add the jokers to the most common card
            while ct > 0 { // iterate down over card counts
                if ccounts[ct as usize] > 0 {
                    ccounts[ct as usize] -= 1;
                    ccounts[(ct+jokers) as usize] += 1;
                    break;
                }
                ct -= 1;
            }
        }
        let hand_type2 = ccounts[5]*10 + ccounts[4]*9 + ccounts[3]*5 + ccounts[2];
        // finished creating the hand
        all_hands.push(Hand {hand_type1, hand_type2, card_order, bid});
    }
    //solution
    all_hands.sort_unstable_by_key(|hand| (hand.hand_type1, hand.card_order));
    let part1: u32 = all_hands.iter_mut().enumerate().map(|(i,hand)| {
        for c in hand.card_order.iter_mut() {
            if *c==10u8 {*c = 0;}  // Jacks become Jokers
        }
        ((i+1) as u32) * hand.bid
    }).sum();
    all_hands.sort_unstable_by_key(|hand| (hand.hand_type2, hand.card_order));
    let part2: u32 = all_hands.iter().enumerate().map(|(i, hand)| ((i+1) as u32)*hand.bid).sum();
    println!("part1: {}\npart2: {}\n", part1, part2);
}
