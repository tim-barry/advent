
const std = @import("std");

const input = @embedFile("input01.txt");

var buf : [20000]u8 = undefined;

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var part1: i32 = 0;
    var part2: i32 = 0;
    //solution
    var left = try std.ArrayList(i32).initCapacity(alloc,1000);
    var right = try std.ArrayList(i32).initCapacity(alloc,1000);
    // read input
    var lines = std.mem.splitScalar(u8, input, '\n');
    while (lines.next()) |line| {
        if (line.len == 0) break; // necessary handle blank line at end (?)
        try left.append(try std.fmt.parseInt(i32, line[0..5], 10));
        try right.append(try std.fmt.parseInt(i32, line[8..], 10));
    }
    // Sort for part 1
    std.sort.block(i32, left.items, {}, std.sort.asc(i32));
    std.sort.block(i32, right.items, {}, std.sort.asc(i32));
    for (left.items, right.items) |l, r| {
        part1 += @intCast(@abs(l - r));
    }
    // part2 (use fact that it is sorted)
    var last: i32 = -1;
    var count: i32 = 0;
    var right_idx: usize = 0;
    for (left.items) |l| {
        if (l == last) {
            part2 += l*count; // Interesting - unnecessary because left happens to have no duplicates
            continue;
        }
        last = l;
        count = 0;
        // scan right until we find match
        while (right_idx < right.items.len and right.items[right_idx] < l) : (right_idx += 1) {}
        // count the number of matches
        while (right_idx < right.items.len and right.items[right_idx] == l) : (right_idx += 1) {
            count += 1;
        }
        part2 += l*count;
    }
    //part2 simpler version
    part2 = 0;
    for (left.items) |l| {
        for (right.items) |r| {
            if (l==r) part2 += l;
        }
    }

    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
