
const std = @import("std");
const input = @embedFile("input05.txt");

const Range = struct {
    i: u64,
    j: u64,
};

pub fn main() !void {
    var buf: [4000]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();
    const w = std.io.getStdOut().writer();

    var maps = std.mem.splitSequence(u8, input, "\n\n");
    const seedstr = maps.next().?;
    var seeds_it = std.mem.splitScalar(u8, seedstr, ' ');
    _ = seeds_it.next(); // drop "seeds:"
    var seeds = try std.ArrayList(struct{s: u64, moved:bool}).initCapacity(alloc, 30);
    var moved = try std.ArrayList(Range).initCapacity(alloc, 100);
    var unmoved = try std.ArrayList(Range).initCapacity(alloc, 100);
    while (seeds_it.next()) |seed_start| {
        const seed_len = seeds_it.next().?;
        const i = try std.fmt.parseInt(u64, seed_start, 10);
        const len = try std.fmt.parseInt(u64, seed_len, 10);
        try unmoved.append(Range{
            .i = i,
            .j = i + len,
        });
        try seeds.append(.{.s=i, .moved=false});
        try seeds.append(.{.s=len, .moved=false});
    }
    // move the ranges and original seeds according to maps
    while (maps.next()) |map| {
        var lines = std.mem.splitScalar(u8, map, '\n');
        _ = lines.next(); // drop description
        while (lines.next()) |map_part| {
            if (map_part.len==0) continue;
            var n_it = std.mem.splitScalar(u8, map_part, ' ');
            const dst = try std.fmt.parseInt(u64, n_it.next().?, 10);
            const src = try std.fmt.parseInt(u64, n_it.next().?, 10);
            const len = try std.fmt.parseInt(u64, n_it.next().?, 10);
            const end = src + len;
            // move seeds according to map part
            for (seeds.items) |*seed| {
                if (seed.moved) continue;
                if (src <= seed.s and seed.s < end) {
                    seed.s +%= dst-%src;
                    seed.moved = true;
                }
            }
            var i: usize = 0;
            while (i < unmoved.items.len) {
                // intersect all ranges with the map part
                const r = unmoved.items[i];
                if (src < r.j and r.i < end) {
                    _ = unmoved.swapRemove(i);
                    const new_r = Range {.i= @max(r.i, src), .j = @min(r.j, end)};
                    if (r.i < new_r.i) {
                        try unmoved.append(.{.i = r.i, .j = new_r.i});
                    }
                    if (new_r.j < r.j) {
                        try unmoved.append(.{.i = new_r.j, .j = r.j});
                    }
                    try moved.append(.{.i = new_r.i - src+dst, .j = new_r.j - src+dst});
                } else {
                    i += 1;
                }
            }
        }
        // finished with this section; collect moved ranges
        try unmoved.appendSlice(moved.items);
        moved.clearRetainingCapacity();
        for (seeds.items) |*seed| {
            seed.moved = false;
        }
    }
    var min_start: u64 = unmoved.items[0].i;
    for (unmoved.items[1..]) |it| {
        if (it.i < min_start) min_start = it.i;
    }
    var min_seed: u64 = seeds.items[0].s;
    for (seeds.items[1..]) |seed| {
        if (seed.s < min_seed) min_seed = seed.s;
    }
    try w.print("part1: {}\npart2: {}\n", .{min_seed, min_start});
}

