
const std = @import("std");

const input = @embedFile("input11.txt");

var buf : [10000]u8 = undefined;

const XY = struct {
    x: usize,
    y: usize,
};

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    const W = std.mem.indexOfScalar(u8, input, '\n').? + 1;
    const H = @divExact(input.len, W);

    var expanded_cols = std.ArrayList(u8).init(alloc);
    for (0..W-1) |x| {
        for (0..H) |y| {
            if (input[y*W + x]=='#') break;
        } else try expanded_cols.append(@intCast(x));
    }
    var expanded_rows = std.ArrayList(u8).init(alloc);
    for (0..H) |y| {
        for (0..W-1) |x| {
            if (input[y*W + x]=='#') break;
        } else try expanded_rows.append(@intCast(y));
    }
    var galaxies = std.ArrayList(XY).init(alloc);
    for (0.., input) |i, c| {
        if (c=='#') try galaxies.append(.{.x = i%W, .y = @divFloor(i,W)});
    }
    var part1: u64 = 0;
    var part2: u64 = 0;
    for (0.., galaxies.items) |i, a| {
        for (galaxies.items[i+1..]) |b| {
            // compute dist a to b and add to part1part2
            var expand: u64 = 0;
            var non_expand: u64 = 0;
            for (@min(a.x, b.x)..@max(a.x, b.x)) |x| {
                if (std.mem.indexOfScalar(u8, expanded_cols.items, @intCast(x)) != null) {
                    expand += 1;
                } else non_expand += 1;
            }
            for (@min(a.y, b.y)..@max(a.y, b.y)) |y| {
                if (std.mem.indexOfScalar(u8, expanded_rows.items, @intCast(y)) != null) {
                    expand += 1;
                } else non_expand += 1;
            }
            part1 += non_expand + 2*expand;
            part2 += non_expand + 1000000*expand;
        }
    }
    //
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
