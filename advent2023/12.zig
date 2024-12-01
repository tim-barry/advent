
const std = @import("std");

const input = @embedFile("input.txt");

// Again use recursion+cache instead of actually working out the DP exactly
// we don't need to generate the full table anyway

const Cache_t = std.AutoHashMap(struct {
    r: u8,
    c: u8,
}, u64);

fn sol1(row_orig: []const u8, counts_orig: []const u8,
        cache: *Cache_t,
        start_row: u8, start_count: u8) u64 {
    // Cache everything
    if (cache.get(.{.r = start_row, .c = start_count})) |cached| return cached;
    var total: u64 = 0;
    defer cache.put(.{.r = start_row, .c = start_count}, total) catch unreachable;
    // for convenience
    const row = row_orig[start_row..];
    const counts = counts_orig[start_count..];
    // have we already placed all the groups?
    if (counts.len==0) { // if there are no damaged parts left, the placement is valid
        total = if (std.mem.indexOfScalar(u8,row,'#')==null) 1 else 0;
        return total;
    }
    // Do the remaining groups fit inside the remaining space?
    var min_squares = counts.len - 1; // minimum empty spaces between the groups
    for (counts) |c| min_squares += c; // totals to the minimum length total: 1,1,3 => #.#.### => 2. + 5# : (3-1)+(1+1+3)
    if (min_squares > row.len) return total; // (0) no, they do not
    // recurse (DP)
    if (row[0] == '#' or row[0] == '?') {
        for (row[0..counts[0]]) |r| {
            if (r=='.') break;
        } else {
            if (counts[0] == row.len) { // this count fits exactly in the rest of the row: must be last
                total = if (counts.len==1) 1 else 0; // wasn't adding to cache correctly
                return total;
            } else if (row[counts[0]]!='#') {
                total += sol1(row_orig, counts_orig, cache, start_row + counts[0] + 1, start_count+1);
            }
        }
    }
    if (row[0] == '.' or row[0] == '?') {
        total += sol1(row_orig, counts_orig, cache, start_row+1, start_count);
    }
    return total;
}

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.GeneralPurposeAllocator(.{}){};
    const alloc = fba.allocator();

    var part1: u64 = 0;
    var part2: u64 = 0;
    var lines_it = std.mem.splitScalar(u8, input, '\n');
    while (lines_it.next()) |line| {
        if (line.len==0) continue;
        const space_i = std.mem.indexOfScalar(u8, line, ' ').?;
        const row = line[0..space_i];
        var counts = std.ArrayList(u8).init(alloc);
        defer counts.deinit();
        var count_it = std.mem.splitScalar(u8, line[space_i+1..], ',');
        while (count_it.next()) |count_s| {
            try counts.append(try std.fmt.parseInt(u8, count_s, 10));
        }
        // replicate the arrays by 5 (adding ? in between the rows)
        var row2 = try std.ArrayList(u8).initCapacity(alloc, row.len*5 + 5);
        defer row2.deinit();
        row2.appendSliceAssumeCapacity(row);
        inline for (0..4) |_| {row2.appendAssumeCapacity('?'); row2.appendSliceAssumeCapacity(row);}
        var counts2 = try std.ArrayList(u8).initCapacity(alloc, counts.items.len*5);
        inline for (0..5) |_| counts2.appendSliceAssumeCapacity(counts.items);
        defer counts2.deinit();
        //
        var cache = Cache_t.init(alloc); // TODO move outside loop?
        defer cache.deinit();
        part1 += sol1(row, counts.items, &cache, 0, 0);
        cache.clearRetainingCapacity();
        part2 += sol1(row2.items, counts2.items, &cache, 0, 0);
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
