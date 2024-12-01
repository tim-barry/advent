// zig 0.4.0 (https://tio.run/#zig)

const std = @import("std");

/// Our Level type: we use 3 bits for each tile
const Level: type = u75;

const left_mask:  Level = 1|1<<15|1<<30|1<<45|1<<60;
const right_mask: Level = left_mask<<12;
const high_mask:  Level = 1|1<<3|1<<6|1<<9|1<<12;
const low_mask:   Level = 1<<60|1<<63|1<<66|1<<69|1<<72;
const bug_mask:   Level = left_mask*high_mask;

const the_middle: Level = 1<<(12*3);
const mids:  [4] u7     = [4]u7   {      7*3,      11*3,       13*3,     17*3};
const masks: [4] Level  = [4]Level{high_mask, left_mask, right_mask, low_mask};

fn printbugs(level: Level) void {
    var i: u7 = 0;
    while (i < 75) {
        var ch: [1]u8 = switch((level>>i) & 1) { 0=>".", 1=>"#", else=>unreachable,};
        std.debug.warn("{}", ch);
        if (i%15 == 12) std.debug.warn("\n");
        i+=3;
    }
}

fn neighbours(level: Level) Level {
    var res: Level = level>>15;       // shift up
    res += (level &~left_mask) >> 3;  // shift left
    res += (level &~right_mask) << 3; // shift right
    res += (level &~low_mask) << 15;  // shift down
    return res;
}

fn next_state(level: Level, adj: Level) Level {
    const count_1 = adj & ~adj>>1 & ~adj>>2 & bug_mask; // cells equal to 1
    const count_2 = ~adj & adj>>1 & ~adj>>2 & bug_mask; // cells equal to 2
    return count_1 | (count_2&~level);
}

// Part 1

fn contains(comptime T: type, arr: []const T, val: T) bool {
   for (arr) |item| if (item==val) return true;
   return false;
}

fn advance_part1(level: Level) Level {
    return next_state(level, neighbours(level));
}

fn b3_to_bio(level: Level) u25 {
    var shift: u7 = 0;
    var bio: u25 = 0;
    var cur = level;
    while (shift<25) : ({shift+=1; cur>>=3;}) {
        bio |= @intCast(u25, (cur&1)<<shift);
    }
    return bio;
}

fn part1(level: Level) void {
    var seen = []Level{0} ** 100;
    var minute: u8 = 0;
    var cur = level;
    while (!contains(Level, seen[0 .. minute], cur)) {
        seen[minute] = cur;
        cur = advance_part1(cur);
        minute += 1;
    }
    std.debug.warn("Part 1: after {} minutes, biodiversity is {}\n", minute, b3_to_bio(cur));
    printbugs(cur);
}

// Part 2

/// Advance a single level based on current and outside/inside state
fn advance_level_part2(curr: Level, prev: Level, next: Level) Level {
    var res: Level = 0;
    //count inner/outer neighbours
    for (masks) |mask, i| {
        res += (Level(@popCount(next & mask))) << mids[i];
        res += mask * (prev>>mids[i] & 1);
    }
    res |= ((res>>2)&bug_mask)*0b11;
    res &= bug_mask|bug_mask<<1;
    // add same-level neighbours (avoiding overflow)
    res += neighbours(curr);
    return next_state(curr, res) & ~the_middle;
}

/// Advance all levels in-place
fn advance_part2(levels: []Level) void {
    var prev: Level = 0;
    var curr: Level = 0;
    var next: Level = 0;
    for (levels) |*level, i| {
        prev = curr;
        curr = level.*;
        next = if (i < levels.len-1) levels[i+1] else 0;
        level.* = advance_level_part2(curr, prev, next);
    }
}

fn part2(start: Level) void {
    var levels = []Level{0} ** 300;
    levels[150] = start;
    var i: u8 = 0;
    while (i<200) : (i+=1) {
        advance_part2(levels[148-i/2 .. 152+i/2]);
    }
    var bugs: u32 = 0;
    for (levels) |level| bugs += @popCount(level);
    std.debug.warn("Part 2: after 200 minutes, number of bugs is {}\n", bugs);
    printbugs(levels[150]);
}


fn read_input() !Level {
    var res: Level = 0;
    const stdin = try std.io.getStdIn();
    var buf = []u8{0}**50;
    _ = try stdin.read(buf[0 .. 50]);
    var i: u7 = 0;
    for (buf) |ch, inp_i| {
        switch (ch) {
            '#' => {res |= ((Level(1))<<i); i+=3;},
            '.' => {i+=3;},
            '\n','\r' => {}, // ignore line ending
            0 => break, // end of input
            else => {
                std.debug.warn("Invalid character {} at position {}\n", ch, inp_i);
                return error.BadInput;
            },
        }
        if (i==75) break; // ignore extra input
    }
    if (i<75) {
        std.debug.warn("Input terminated early: read {} of required 25 cells\n", i/3);
        return error.BadInput;
    }
    return res;
}

pub fn main() !void {
    const my_input = try read_input();
    part1(my_input);
    part2(my_input);
}
