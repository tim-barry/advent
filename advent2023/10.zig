
const std = @import("std");

const input = @embedFile("input.txt");

var buf : [20000]u8 = undefined;

const FloodFill = enum{
    unset,
    line,
    left,
    right,
};

const dir_name = [_][]const u8{"right", "down", "left", "up"};

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    //parse input
    const W: i32 = @intCast(std.mem.indexOfScalar(u8, input, '\n').? + 1);
    const S: i32 = @intCast(std.mem.indexOfScalar(u8, input, 'S').?);
    var flood = [_]FloodFill{.unset} ** input.len;

    var path = std.ArrayList(i8).init(alloc);
    defer path.deinit();

    const d = [4]i32{1, W, -1, -W};  // clockwise from right
    var turns: i8 = 0;
    for (0..4) |start_dir| {
        try path.append(@intCast(start_dir));
        var prev_dir = start_dir;
        // var prev_p = S;
        var cur_p = S + d[start_dir];
        turns = 0;
        // try w.print("start dir {} ({s})\n", .{start_dir, dir_name[start_dir]});
        while (cur_p != S) {
            // have: cur_p, prev_dir
            const c = input[@intCast(cur_p)];
            // try w.print("cur_p: {} (x: {}, y: {}), c: {c}\n", .{cur_p, @mod(cur_p,W),@divFloor(cur_p,W), c});
            const cur_dir: usize = switch(c) {
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
        // try w.print("No path: exited after {} steps\n", .{path.items.len});
        path.clearRetainingCapacity();
    } else unreachable;
    // retrace the path from
    const part1 = @divExact(path.items.len, 2);
    const winding_dir = if (turns > 0) "Right" else "Left"; // +4 = cw ('Right' is inside), -4 = ccw
    var p2p: i32 = S;
    var prev_dir: i8 = path.items[0];
    for (path.items[1..]) |turn| {
        p2p += d[@intCast(prev_dir)];
        flood[@intCast(p2p)] = .line;
        const left_p = p2p +     d[@intCast(@mod(prev_dir-1, 4))];
        const straight_p = p2p + d[@intCast(prev_dir)];
        const right_p = p2p +    d[@intCast(@mod(prev_dir+1, 4))];
        if (flood[@intCast(left_p)] != .line) flood[@intCast(left_p)] = switch(turn) {
            -1 => .line,
            0,1 => .left,
            else => unreachable,
        };
        if (flood[@intCast(straight_p)] != .line) flood[@intCast(straight_p)] = switch(turn) {
            -1 => .right,
            0 => .line,
            1 => .left,
            else => unreachable,
        };
        if (flood[@intCast(right_p)] != .line) flood[@intCast(right_p)] = switch(turn) {
            -1,0 => .right,
            1 => .line,
            else => unreachable,
        };
        prev_dir = @intCast(@mod(prev_dir+turn, 4));
    }
    // do the flood fill
    var done = false;
    while (!done) {
        done = true;
        for (0.., &flood) |i, *f| {
            if (input[i]=='\n') continue;
            if (f.* == .unset) {
                for (0..4) |dir| {
                    const p: i32 = @as(i32,@intCast(i))+d[dir];
                    if (p < 0 or p >= input.len or input[@intCast(p)]=='\n') continue; //oob
                    const u_p: usize = @intCast(p);
                    if (flood[u_p]==.left) {
                        f.* = .left;
                        break;
                    }
                    if (flood[u_p]==.right) {
                        f.* = .right;
                        break;
                    }
                } else done = false;
            }
        }
    }
    var left: u32 = 0;
    var right: u32 = 0;
    for (&flood) |f| {
        if (f==.left) left +=1;
        if (f==.right) right +=1;
    }

    //
    try w.print("part1: {}\npart2: {} on Left, {} on Right. The inside is {s}\n",
     .{part1, left, right, winding_dir});
}
