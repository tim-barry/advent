const std = @import("std");

//AA=0
//'AA', 'AI', 'AQ', 'AZ', 'HA', 'HC', 'IM', 'IY', 'KQ', 'KZ', 'LS', 'QK', 'RF', 'VI', 'YC', 'ZJ'
//
const Pos: type = u64;
const Score: type = i64;
const Idx: type = u32;
const Time: type = i8;

const globl_cost = [16][]const Time{ // Distance array
    &[16]Time{ 0, 6, 11, 7, 9, 6, 11, 9, 2, 3, 3, 2, 5, 9, 4, 2 },
    &[16]Time{ 6, 0, 15, 11, 13, 4, 15, 13, 8, 6, 7, 4, 9, 13, 2, 5 },
    &[16]Time{ 11, 15, 0, 4, 2, 15, 3, 2, 9, 9, 11, 11, 6, 5, 13, 12 },
    &[16]Time{ 7, 11, 4, 0, 2, 11, 4, 2, 5, 5, 7, 7, 2, 2, 9, 8 },
    &[16]Time{ 9, 13, 2, 2, 0, 13, 3, 2, 7, 7, 9, 9, 4, 3, 11, 10 },
    &[16]Time{ 6, 4, 15, 11, 13, 0, 15, 13, 8, 6, 7, 4, 9, 13, 2, 5 },
    &[16]Time{ 11, 15, 3, 4, 3, 15, 0, 2, 9, 9, 11, 11, 6, 3, 13, 12 },
    &[16]Time{ 9, 13, 2, 2, 2, 13, 2, 0, 7, 7, 9, 9, 4, 3, 11, 10 },
    &[16]Time{ 2, 8, 9, 5, 7, 8, 9, 7, 0, 4, 2, 4, 3, 7, 6, 4 },
    &[16]Time{ 3, 6, 9, 5, 7, 6, 9, 7, 4, 0, 2, 2, 3, 7, 4, 3 },
    &[16]Time{ 3, 7, 11, 7, 9, 7, 11, 9, 2, 2, 0, 3, 5, 9, 5, 3 },
    &[16]Time{ 2, 4, 11, 7, 9, 4, 11, 9, 4, 2, 3, 0, 5, 9, 2, 2 },
    &[16]Time{ 5, 9, 6, 2, 4, 9, 6, 4, 3, 3, 5, 5, 0, 4, 7, 6 },
    &[16]Time{ 9, 13, 5, 2, 3, 13, 3, 3, 7, 7, 9, 9, 4, 0, 11, 10 },
    &[16]Time{ 4, 2, 13, 9, 11, 2, 13, 11, 6, 4, 5, 2, 7, 11, 0, 3 },
    &[16]Time{ 2, 5, 12, 8, 10, 5, 12, 10, 4, 3, 3, 2, 6, 10, 3, 0 },
};

const CostTbl: type = []const []const Time;

// max recursion depth is 16
fn max_pressure_slice(cost: CostTbl, nodes: []bool, curr: u5, time: Time) Score {
    if (time <= 0) unreachable;
    var max_sub: Score = 0;
    for (nodes) |*node, idx| {
        if (!node.*) continue;
        const next_time = time - cost[curr][idx] - 1;
        if (next_time <= 0) continue;
        node.* = false;
        const tScore = max_pressure_slice(cost, nodes, idx, next_time);
        if (tScore > max_sub) max_sub = tScore;
        node.* = true;
    }
    return max_sub + benefit[curr] * @intCast(u8, time);
}

fn max_pressure_bits(cost: CostTbl, nodes: u32, curr: u5, time: Time) Score {
    if (time <= 0) unreachable;
    var max_sub: Score = 0;
    var idx: u5 = 0;
    var thebit: u32 = @as(u32, 1) << idx;
    while (nodes >= thebit) : ({
        idx += 1;
        thebit <<= 1;
    }) {
        if (nodes & thebit == 0) continue;
        const next_time = time - cost[curr][idx] - 1;
        if (next_time <= 0) continue;
        const tScore = max_pressure_bits(cost, nodes & ~thebit, idx, next_time);
        if (tScore > max_sub) max_sub = tScore;
    }
    return max_sub + benefit[curr] * @intCast(u8, time);
}

const benefit = [16]Score{ 0, 25, 23, 20, 12, 24, 19, 15, 17, 5, 3, 10, 18, 22, 9, 6 };

fn part1(nodeCount: u5, cost: CostTbl) Score {
    return max_pressure_bits(cost, (@as(u32, 1) << nodeCount) - 2, 0, 30);
}

fn part2(nodeCount: u5, cost: CostTbl, alloc: std.mem.Allocator) !Score {
    const nodesLimit2 = (@as(u32, 1) << nodeCount);
    const nonAAnodes = (@as(u32, 1) << nodeCount) - 2;
    var maxPressure = std.AutoHashMap(u32, Score).init(alloc);
    defer maxPressure.deinit();
    const subset_low: u5 = nodeCount / 2;
    const subset_high: u5 = if (nodeCount & 1 == 0) subset_low else subset_low + 1;
    const subset_min: u5 = subset_low - 1; // 6
    const subset_max: u5 = subset_high + 1; // 9
    var nodeset: u32 = 0b10;
    while (nodeset < nodesLimit2) : (nodeset += 2) {
        const ppct = @popCount(nodeset);
        if (ppct > subset_max or ppct < subset_min) continue;
        const pres = max_pressure_bits(cost, nodeset, 0, 26);
        try maxPressure.putNoClobber(nodeset, pres);
    }
    var mtot: Score = 0;
    var it = maxPressure.keyIterator();
    while (it.next()) |nodes| {
        if (@popCount(nodes.*) < subset_high) continue;
        const other = maxPressure.get(nonAAnodes ^ nodes.*) orelse continue;
        const ttot = maxPressure.get(nodes.*).? + other;
        if (ttot > mtot) mtot = ttot;
    }
    return mtot;
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    var nodeCount: u5 = 16;
    var cost = &globl_cost;
    // TODO: parse input into graph, [][]cost, []benefit, nodeset
    std.debug.print("{}\n", .{part1(nodeCount, cost)});
    std.debug.print("{}\n", .{try part2(nodeCount, cost, allocator)});
}
