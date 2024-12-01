
use num::integer::binomial;
use to_vec::toVecResult;

// Unfinished and untested

const input = include_str!("input09.txt");

pub fn main() !void {
    let part1: i32 = 0;
    let part2: i32 = 0;
    //solution
    let hists = input.lines().map(|line| line.split(' ').map(i32::from_str).to_vec_result().unwrap());
    let coefs = hists.map(|hist| {
        let L = hist.len();
        let mut coef: Vec<i32> = vec![];
        while !hist.iter().all(|x| x==0) {
            coef.push(hist[0]);
            for i in 0..hist.len()-1 {
                hist[i] = hist[i+1]-hist[i];
            }
            hist.pop();
        }
        (L,coef)
    });
    for coef in coefs {
        for (i,(L,c)) in coef.iter().enumerate() {
            part1 += c * binomial(L, i)));
        }
        //part2
        let mut res: i32 = 0;
        for i in 0..coef.len() {
            res = coef[coef.len()-i-1] - res;
        }
        part2 += res;
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
