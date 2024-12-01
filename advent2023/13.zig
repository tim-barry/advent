
const std = @import("std");

const input = @embedFile("input13.txt");

var buf : [1000]u8 = undefined;

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var part1: u64 = 0;
    var part2: u64 = 0;
    // Brute force is easily fast enough when we exit early
    // probably even if we don't
    var grids_it = std.mem.split(u8, input, "\n\n");
    while (grids_it.next()) |grid| {
        var lines = std.ArrayList([]const u8).init(alloc);
        // defer lines.deinit();
        var line_it = std.mem.splitScalar(u8, grid, '\n');
        while (line_it.next()) |line| if (line.len>0) try lines.append(line);
        const H = lines.items.len;
        const W = lines.items[0].len;
        // check horizontal reflection line
        for (1..H) |refl| {
            const refl_len = @min(refl, H-refl);
            var diff_count: u8 = 0;
            for (0..refl_len) |dy| { // rows are reflected; check each row pair
                for (0..W) |x| { // check each column
                    if (lines.items[refl+dy][x]!=lines.items[refl-dy-1][x]) diff_count += 1;
                }
                if (diff_count > 1) break;
            } else switch(diff_count) {0 => part1 += refl*100, 1 => part2 += refl*100, else=>unreachable,}
        }
        // check vertical reflection lines
        for (1..W) |refl| {
            const refl_len = @min(refl, W-refl);
            var diff_count: u8 = 0;
            for (0..refl_len) |dx| { // cols are reflected; check each column pair
                for (0..H) |y| { // check each row
                    if (lines.items[y][refl+dx]!=lines.items[y][refl-dx-1]) diff_count += 1;
                }
                if (diff_count > 1) break;
            } else switch(diff_count) {0 => part1 += refl, 1 => part2 += refl, else=>unreachable,}
        }
        fba.reset();
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
