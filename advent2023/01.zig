
const std = @import("std");

const input = @embedFile("input01.txt");

const digits: [10][2][]const u8 = .{
    .{"0","zero"},
    .{"1","one"},
    .{"2","two"},
    .{"3","three"},
    .{"4","four"},
    .{"5","five"},
    .{"6","six"},
    .{"7","seven"},
    .{"8","eight"},
    .{"9","nine"},
};

fn first_last(line: []const u8, part: u8) u8 {
    var first_p: usize = line.len+1;
    var last_p: usize = 0;
    var first: u8 = 0;
    var last: u8 = 0;
    for (0.., digits) |i, dig| {
        for(0..part) |p| {
            const f = std.mem.indexOf(u8, line, dig[p]);
            const l = std.mem.lastIndexOf(u8, line, dig[p]);
            if (f != null and f.? < first_p) {
                first_p = f.?;
                first = @intCast(i);
            }
            if (l != null and l.? >= last_p) {
                last_p = l.?;
                last = @intCast(i);
            }
        }
    }
    return first*10 + last;
}

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    var part1: u32 = 0;
    var part2: u32 = 0;
    var it = std.mem.splitScalar(u8, input, '\n');
    while (it.next()) |line| {
        part1 += first_last(line, 1);
        part2 += first_last(line, 2);
    }
    try stdout.print("{}\n{}\n",.{part1, part2});
}