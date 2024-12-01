
const std = @import("std");
const input = @embedFile("input04.txt");

pub fn main() !void {
    const w = std.io.getStdOut().writer();

    var line_it = std.mem.splitScalar(u8, input, '\n');
    var buf: [100]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    // part2 'lookahead' up to 10 (max number of matches)
    var next_card_counts: [10]u32 = [_]u32{1}**10;
    var card_i: u8 = 0;

    var part1: u32 = 0;
    var part2: u32 = 0;
    while (line_it.next()) |line| {
        if (line.len < 2) { continue; }
        // parse line and count matches
        var matches: u5 = 0; // <=10
        var set = std.AutoHashMap(u8, void).init(alloc);
        defer fba.reset();
        // defer set.deinit();
        var i: usize = 0;
        while (line[i]!=':') : (i += 1) {}
        var num_it = std.mem.splitScalar(u8, line[i+1..], ' ');
        while (num_it.next()) |chunk| {
            if (chunk.len==0) continue;
            if (chunk[0]=='|') break;
            const n = try std.fmt.parseInt(u8, chunk, 10);
            try set.put(n, {});
        }
        while (num_it.next()) |chunk| {
            if (chunk.len==0) continue;
            const n = try std.fmt.parseInt(u8, chunk, 10);
            if (set.contains(n)) {
                matches += 1;
            }
        }
        // now have matches
        if (matches > 0) {
            part1 += @as(u32, 1)<<(matches-1);
        }
        // get count of this card for part2
        const this_card_count = next_card_counts[card_i%10];
        part2 += this_card_count;
        next_card_counts[card_i%10] = 1;
        for (1..matches+1) |won_card| {
            next_card_counts[(card_i + won_card)%10] += this_card_count;
        }
        card_i += 1;
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}

