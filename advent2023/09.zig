
const std = @import("std");

const input = @embedFile("input09.txt");

var buf : [2000]u8 = undefined;

// pub fn any(comptime T: type, arr: []const T) bool {
//     switch(@typeInfo(T)) {
//         .Int => {
//             for (arr) |item| {
//                 if (item != 0) return true;
//             } else return false;
//         },
//         else => @compileError("not implemented"),
//     }
// }

fn comb(comptime T: type, n:T, k:T) T {
    // n!/(k! n-k!)
    if (n < 0 or k < 0) unreachable;
    var ret: T = 1;
    const lo: T = @min(k, n-k);
    const hi: T = @max(k, n-k);
    for (@as(usize,@intCast(hi+1))..@as(usize,@intCast(n+1)), 1..@as(usize,@intCast(lo+1))) |num, den| {
        ret *= @intCast(num);
        ret = @divExact(ret, @as(T, @intCast(den)));
    }
    return ret;
}

test "comb" {
    try std.testing.expectEqual(comb(i32, 2, 0), 1);
    try std.testing.expectEqual(comb(i32, 2, 1), 2);
    try std.testing.expectEqual(comb(i32, 2, 2), 1);
    try std.testing.expectEqual(comb(i32, 4, 0), 1);
    try std.testing.expectEqual(comb(i32, 4, 1), 4);
    try std.testing.expectEqual(comb(i32, 4, 2), 6);
    try std.testing.expectEqual(comb(i32, 4, 3), 4);
    try std.testing.expectEqual(comb(i32, 4, 4), 1);
    try std.testing.expectEqual(comb(i32, 5, 0), 1);
    try std.testing.expectEqual(comb(i32, 5, 1), 5);
    try std.testing.expectEqual(comb(i32, 5, 2), 10);
    try std.testing.expectEqual(comb(i32, 5, 3), 10);
    try std.testing.expectEqual(comb(i32, 5, 4), 5);
    try std.testing.expectEqual(comb(i32, 5, 5), 1);
}

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var part1: i32 = 0;
    var part2: i32 = 0;
    //solution
    var line_it = std.mem.splitScalar(u8, input, '\n');
    while (line_it.next()) |line| {
        // try w.print("parsing line: {s}\n", .{line});
        if (line.len==0) continue;
        // Parse the input line
        var arr = std.ArrayList(i32).init(alloc);
        var int_it = std.mem.splitScalar(u8, line, ' ');
        while (int_it.next()) |int| {
            // try w.print("parsing int: {s}, {any}\n", .{int, int});
            try arr.append(try std.fmt.parseInt(i32, int, 10));
        }
        const L = arr.items.len;
        // Generate 'coefficients' from the input
        var coef = std.ArrayList(i32).init(alloc);
        while (!std.mem.allEqual(i32, arr.items, 0)) {
            try coef.append(arr.items[0]);
            for (0.., arr.items[0..arr.items.len-1]) |i, *it| {
                // try w.print("adding: coef={any}, items={any}, i={}\n", .{coef, arr.items, i});
                it.* = arr.items[i+1] - it.*;
            }
            _ = arr.pop();
        }
        // with the coefficients, compute the solution to part1+part2
        for (0.., coef.items) |i, c| {
            part1 += c * @as(i32, @intCast(comb(usize, L, i)));
        }
        //part2
        var res: i32 = 0;
        for (0..coef.items.len) |i| {
            res = coef.items[coef.items.len-i-1] - res;
        }
        part2 += res;
        fba.reset();
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
