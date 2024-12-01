
const std = @import("std");

const input = @embedFile("input.txt");

var buf : [20000]u8 = undefined;

const Side = enum{
    unset,
    line,
    left,
    right,
};

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    //parse input
    const W: i32 = @intCast(std.mem.indexOfScalar(u8, input, '\n').? + 1);
    const S: i32 = @intCast(std.mem.indexOfScalar(u8, input, 'S').?);
    var flood = [_]Side{.unset} ** input.len;

    var path = std.ArrayList(i8).init(alloc);
    defer path.deinit();

    const d = [4]i32{1, W, -1, -W};  // clockwise from right
    var turns: i8 = 0;
    var the_start_dir: usize = undefined;
    for (0..4) |start_dir| {
        the_start_dir = start_dir;
        var prev_dir: u2 = @intCast(start_dir);
        var cur_p = S + d[prev_dir];
        turns = 0;
        while (cur_p != S) {
            const c = input[@intCast(cur_p)];
            const cur_dir: u2 = switch(c) {
                '|' => if (prev_dir==1 or prev_dir==3) prev_dir else break,
                '-' => if (prev_dir==0 or prev_dir==2) prev_dir else break,
                '7' => if (prev_dir==0) 1 else if (prev_dir==3) 2 else break,
                'J' => if (prev_dir==1) 2 else if (prev_dir==0) 3 else break,
                'L' => if (prev_dir==2) 3 else if (prev_dir==1) 0 else break,
                'F' => if (prev_dir==3) 0 else if (prev_dir==2) 1 else break,
                '.' => break,
                else => unreachable,
            };
            const this_turn: i8 = switch(c) {
                '|','-' => 0,
                '7' => if (prev_dir==0) 1 else -1,
                'J' => if (prev_dir==1) 1 else -1,
                'L' => if (prev_dir==2) 1 else -1,
                'F' => if (prev_dir==3) 1 else -1,
                else => unreachable,
            };
            turns += this_turn;
            const next_p = cur_p + d[cur_dir];
            try path.append(this_turn);

            if (next_p < 0 or next_p >= input.len or input[@intCast(next_p)]=='\n') break; // out of bounds
            // prev_p = cur_p;
            prev_dir = cur_dir;
            cur_p = next_p;
        }
        if (cur_p == S) { // found path
            try w.print("Found path\n", .{});
            break;
        }
        path.clearRetainingCapacity();
    } else unreachable;
    const part1 = @divExact(path.items.len + 1, 2); // add 1 because we don't count the initial move at S as a turn
    const inside: Side = if (turns > 0) .right else .left; // + = cw ('Right' is inside), - = ccw
    // retrace the path and set everything on its left and right
    var p2p: i32 = S;
    var prev_dir: u2 = @intCast(the_start_dir);
    for (path.items) |turn| {
        p2p += d[@intCast(prev_dir)];
        flood[@intCast(p2p)] = .line;
        const left_p:     usize = @intCast(p2p + d[prev_dir-%1]);
        const straight_p: usize = @intCast(p2p + d[prev_dir]);
        const right_p:    usize = @intCast(p2p + d[prev_dir+%1]);
        if (flood[left_p] != .line) flood[left_p] = switch(turn) {
            -1 => .line,
            0,1 => .left,
            else => unreachable,
        };
        if (flood[straight_p] != .line) flood[straight_p] = switch(turn) {
            -1 => .right,
            0 => .line,
            1 => .left,
            else => unreachable,
        };
        if (flood[right_p] != .line) flood[right_p] = switch(turn) {
            -1,0 => .right,
            1 => .line,
            else => unreachable,
        };
        prev_dir = prev_dir +% @as(u2, @intCast(turn&0b11));
    }
    var inside_count: u32 = 0;
    var outside_count: u32 = if(flood[0]==.line) 0 else 1;
    for (1..flood.len) |i| {
        if (input[i]=='\n') continue;
        switch(flood[i]) {
            .left, .right => {
                inside_count += if (flood[i]==inside) 1 else 0;
                outside_count += if (flood[i]==inside) 0 else 1;
            },
            .line => {},
            .unset => {
                const prev: usize = i-1;
                if (flood[prev]==inside) {
                    flood[i] = inside;
                    inside_count += 1;
                } else outside_count += 1;
            }
        }
    }
    try w.print("part1: {}\npart2: {} inside\n", .{part1, inside_count});
}
