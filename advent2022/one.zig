//
// one
// Zig version: 0.10.0
// Date: 2022-11-30
//

const std = @import("std");

const F = "input1.txt";
const s = @embedFile(F);
const elves_comp = comptime std.mem.count(u8, s, "\n\n");


pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const alloc = arena.allocator();

    const n_elves = std.mem.count(u8, s, "\n\n");
    var l = std.ArrayList(u64).init(alloc);
    var it = std.mem.split(u8, s, "\n\n");
    while (it.next()) |elf| {
        const i: u64 = 0;
        while (elf.next()) |n| {
            i += try std.fmt.parseInt(u64, n, 10);
        }
        l.append(i);
    }
    std.sort.sort(u64, l.items);
    std.debug.print("{}\n", .{l.at});
}
