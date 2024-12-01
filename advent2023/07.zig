
const std = @import("std");

const input = @embedFile("input0700.txt");

var buf : [20000]u8 = undefined;

const Hand = struct {
    hand_type1: u8,
    hand_type2: u8,
    card_order: [5]u8,
    bid: u32,
};

fn lessThan1(ctx: void, a: Hand, b: Hand) bool {
    _ = ctx;
    return (a.hand_type1 < b.hand_type1)
    or (a.hand_type1 == b.hand_type1 and std.mem.lessThan(u8, &a.card_order, &b.card_order));
}
fn lessThan2(ctx: void, a: Hand, b: Hand) bool {
    _ = ctx;
    return (a.hand_type2 < b.hand_type2)
    or (a.hand_type2 == b.hand_type2 and std.mem.lessThan(u8, &a.card_order, &b.card_order));
}

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var all_hands = std.ArrayList(Hand).init(alloc);

    var part1: u64 = 0;
    var part2: u64 = 0;
    // read input
    var lines = std.mem.splitScalar(u8, input, '\n');
    while (lines.next()) |line| {
        if (line.len==0) continue;
        //
        const hand = line[0..5];
        const bid = try std.fmt.parseInt(u32, line[6..], 10);
        var h = Hand{.hand_type1 = undefined, .hand_type2 = undefined, .card_order = undefined, .bid = bid};
        var counts = [_]u8{0}**15; // count of each card
        var ccounts = [_]u8{13, 0, 0, 0, 0, 0}; // most_common structure
        for (0.., hand) |ci, c| {
            const value: u8 = switch(c) {
                '2'...'9' => c-'1', // 1...8
                'A' => 13,
                'K' => 12,
                'Q' => 11,
                'J' => 10,
                'T' => 9,
                else => unreachable,
            };
            h.card_order[ci] = value;
            ccounts[counts[value]] -= 1;
            counts[value] += 1;
            ccounts[counts[value]] += 1;
        }
        h.hand_type1 = ccounts[5]*10 + ccounts[4]*9 + ccounts[3]*5 + ccounts[2];
        // hand_type2
        const jokers = counts[10];
        if (0 < jokers and jokers < 5) {
            ccounts[jokers] -= 1;
            var ct: u8 = 4;
            // we add the jokers to the most common card
            while (ct > 0) : (ct -= 1) { // iterate down over card counts
                if (ccounts[ct] > 0) {
                    ccounts[ct] -= 1;
                    ccounts[ct+jokers] += 1;
                    break;
                }
            }
        }
        h.hand_type2 = ccounts[5]*10 + ccounts[4]*9 + ccounts[3]*5 + ccounts[2];
        // finished creating the hand
        try all_hands.append(h);
    }
    //solution
    std.sort.heap(Hand, all_hands.items, {}, lessThan1);
    for (1.., all_hands.items) |i, *hand| {
        part1 += i * hand.bid;
        for (&hand.card_order) |*c| {
            if (c.*==10) c.* = 0;  // Jacks become Jokers
        }
    }
    std.sort.heap(Hand, all_hands.items, {}, lessThan2);
    for (1.., all_hands.items) |i, hand| {
        part2 += i * hand.bid;
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
