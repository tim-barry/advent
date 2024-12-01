
const std = @import("std");

// manually managed circular buffer to store gears
var nums: [20]u32 = undefined;
var gear_pos: [20]usize = undefined;
var start: usize = 0;
var end: usize = 0;
//var data_size: usize = end-start; // stats: maximum resident set is 12 for my input; O(20) should be enough

fn solution(s: []const u8) !void {
    const stdout = std.io.getStdOut();
    const w = stdout.writer();
    // indices into s
    var i: usize = 0;
    var j: usize = 0;
    const W: usize = std.mem.indexOfScalar(u8, s, '\n').? + 1;

    var part1: u32 = 0;
    var part2: u32 = 0;
    while (i < s.len) : (i += 1) { // parse all the numbers and sum the totals online
        if ('0'<=s[i] and s[i]<='9') {
            j = i+1;
            while ('0' <= s[j] and s[j] <= '9') : (j += 1) {}
            // check all nearby positions for a symbol
            var has_symbol: bool = false;
            var gear_p: usize = 0;
            for (0..3) |y| {
                for (i-1..j+1) |x| {
                    const np: i32 = (@as(i32, @intCast(y))-1)*@as(i32,@intCast(W)) + @as(i32,@intCast(x));
                    if (np < 0 or np > s.len) continue;
                    const p: usize = @intCast(np);
                    if (s[p] != '.' and (s[p]<'0' or s[p]>'9') and s[p]!='\n') {
                        has_symbol = true;
                        if (s[p]=='*') gear_p = p;
                    }
                }
            }
            if (has_symbol) {
                const n: u32 = try std.fmt.parseInt(u32, s[i..j], 10);
                part1 += n;
                if (gear_p != 0) { // part 2
                    // small resident set size makes linear search in a circular buffer fast enough
                    // although maybe not as terse as a hashmap
                    for (start..end) |stored| { // search in DB
                        if (gear_pos[stored%20]==gear_p) { // next to the same gear (assume only 2 nums can be)
                            part2 += nums[stored%20] * n;
                            if (stored == start) start += 1; // remove (consume)
                            break;
                        } else if ((i > 2*W) and (gear_pos[stored%20] < i - W) and start==stored) {
                            start += 1; // remove (can no longer be matched)
                        }
                    } else { // insert to DB
                        gear_pos[end%20] = gear_p;
                        nums[end%20] = n;
                        end += 1;
                    }
                }
            } //has_symbol
            i = j;
        } // finished parsing a number s[i..j]
    }
    try w.print("{}\n{}\n", .{part1, part2});
}

const input = @embedFile("input03.txt");

pub fn main() !void {
    try solution(input);
}
