const std = @import("std");
const parseInt = std.fmt.parseInt;

const input = @embedFile("input.txt");

const short: type = i16;
const Arr: type = std.ArrayList(short);
const PT: type = u15;
const Perm: type = std.ArrayList(PT);

fn find(comptime T: type, slice: []T, item: T) u15 {
    for (slice) |sitem, idx| if (sitem == item) return @intCast(u15, idx);
    unreachable; // return -1;
}

fn move_item(comptime T: type, slice: []T, src: u16, dst: u16) void {
    const item: T = slice[src];
    if (src == dst) return;
    if (src < dst) {
        for (slice[src..dst]) |*it, i| it.* = slice[src + i + 1];
    } else {
        for (slice[src..dst]) |_, i| slice[src - i] = slice[src - i - 1];
    }
    slice[dst] = item;
}

fn mixPerm(data: Arr, perm: Perm) void {
    for (data.items) |dist, idx| {
        // find position of idx in perm
        const src = find(PT, perm.items, @intCast(PT, idx));
        const dst = @intCast(u15, @mod(src + dist, @intCast(short, perm.items.len - 1)));
        // move the item
        move_item(PT, perm.items, src, dst);
    }
}

fn coordSum(data: []short, perm: []PT) i64 {
    const zorig = find(short, data, 0);
    const znew = find(PT, perm, zorig);
    var total: i64 = 0;
    inline for (.{ 1000, 2000, 3000 }) |d| {
        const pos = perm[@intCast(u16, @mod(znew + d, perm.len))];
        total += data[pos];
    }
    return total;
}

fn makePerm(len: usize, alloc: std.mem.Allocator) !Perm {
    var p = try Perm.initCapacity(alloc, len);
    for (p.items) |*item, idx| item.* = @intCast(PT, idx);
    return p;
}

fn part1(data: Arr, perm: Perm) i64 {
    mixPerm(data, perm);
    return coordSum(data.items, perm.items);
}

fn part2(data: Arr, perm: Perm) i64 {
    for ([_]void{{}} ** 10) |_| mixPerm(data, perm);
    return coordSum(data.items, perm.items);
}

pub fn main() !void {
    // parse input
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    //defer _ = gpa.deinit();
    const alloc = gpa.allocator();
    var data = Arr.init(alloc);
    var it = std.mem.split(u8, input, "\n");
    while (it.next()) |line| {
        if (line.len == 0) break;
        try data.append(try parseInt(short, line, 10));
    }
    const Len: u15 = @intCast(u15, data.items.len);
    var data2 = try data.clone();
    const key: u32 = 811589153;
    const key_short: i16 = @intCast(i16, @mod(key, Len - 1));
    for (data2.items) |*item| item.* = @intCast(i16, @mod(@as(i32, item.*) * key_short, Len - 1));
    //defer data.deinit(); // data must be non-const
    var perm = try makePerm(Len, alloc);
    defer perm.deinit();
    std.debug.print("part 1: {}\n", .{part1(data, perm)});
    var perm2 = try makePerm(Len, alloc);
    defer perm2.deinit();
    std.debug.print("part 2: {}\n", .{part2(data2, perm2)});
}
