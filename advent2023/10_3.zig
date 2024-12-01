
const std = @import("std");

const input = @embedFile("input.txt");

var buf : [40000]u8 = undefined;

const Side = enum{
    unset,
    line,
    // left,
    // right,
};

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    //parse input
    const W: i16 = @intCast(std.mem.indexOfScalar(u8, input, '\n').? + 1);
    const S: i16 = @intCast(std.mem.indexOfScalar(u8, input, 'S').?);
    var flood = [_]Side{.unset} ** input.len;

    var path = std.ArrayList(i16).init(alloc);
    defer path.deinit();

    const d = [4]i16{1, W, -1, -W};  // clockwise from right
    var prev_dir: u2 = undefined;
    var start_dir: u2 = 0;
    for (0..4) |_| {
        prev_dir = start_dir;
        var cur_p = S + d[prev_dir];
        try path.append(S);
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
            try path.append(cur_p);

            const next_p = cur_p + d[cur_dir];
            if (next_p < 0 or next_p >= input.len or input[@intCast(next_p)]=='\n') break; // out of bounds
            prev_dir = cur_dir;
            cur_p = next_p;
        }
        if (cur_p == S) { // found path
            try w.print("Found path\n", .{});
            break;
        }
        path.clearRetainingCapacity();
        start_dir += 1;
    } else unreachable;
    const S_actual = ([4][]const u8{"-7.J", "L|J.", ".F-L","F.7|"})[prev_dir][start_dir];
    const part1 = @divExact(path.items.len, 2);
    // retrace the path
    for (path.items) |pos| {
        flood[@intCast(pos)] = .line;
    }
    var inside_count: u16 = 0;
    var outside_count: u16 = if(flood[0]==.line) 0 else 1;
    var intersections: u16 = 0;
    var last_int: u8 = 0;
    for (0..flood.len) |i| {
        if (input[i]=='\n') continue;
        switch(flood[i]) {
            .unset => {
                inside_count += intersections&1;
                outside_count += ~intersections&1;
            },
            .line => switch(if (input[i]=='S') S_actual else input[i]) {
                '|' => intersections += 1,
                '-' => {},
                'L','F' => last_int = input[i],
                'J' => intersections += if (last_int=='F') 1 else 0,
                '7' => intersections += if (last_int=='L') 1 else 0,
                else => unreachable,
            },
        }
    }
    try w.print("part1: {}\npart2: {} inside\n", .{part1, inside_count});
}
