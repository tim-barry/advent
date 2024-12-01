
const std = @import("std");

const input = @embedFile("input.txt");

var buf : [1000]u8 = undefined;

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var part1: u64 = 0;
    var part2: u64 = 0;
    //solution
    //
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
