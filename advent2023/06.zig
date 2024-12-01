
const std = @import("std");

const input = @embedFile("input06.txt");

fn ways(time: u64, dist: u64) u64 {
    // Assume that all races are winnable
    // solve [y = x*(t-x) - dist]   => Quadratic formula, coefficients: a=-1, b=t, c=dist
    //const intercept_left = (+time - sqrt(time*time + 4*dist)) /2 ;
    const intercept_dist = std.math.sqrt(time*time - 4*dist); // rounds down
    // round back up if necessary, to ensure opposite parity from `time` (known and obvious constraint)
    return intercept_dist + (1&(~intercept_dist^time));
}

var buf : [1000]u8 = undefined;

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var part1: u64 = 1;
    var part2: u64 = 0;
    //solution
    var lines = std.mem.splitScalar(u8, input, '\n');
    var data: [2]std.ArrayList(u64) = undefined;
    var pt2 = [2]u64 {0, 0};
    for (0..2) |i| {
        data[i] = std.ArrayList(u64).init(alloc);
        const line = lines.next().?;
        var n_it = std.mem.tokenizeScalar(u8, line, ' ');
        _ = n_it.next();
        while (n_it.next()) |n_s| {
            for (n_s) |dig| {
                pt2[i] *= 10;
                pt2[i] += dig-'0';
            }
            try data[i].append(try std.fmt.parseInt(u64, n_s, 10));
        }
    }
    // part 1:
    for (0.., data[0].items) |i, time| {
        part1 *= ways(time, data[1].items[i]);
    }
    part2 = ways(pt2[0], pt2[1]);
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
