
const std = @import("std");

const input = @embedFile("input.txt");

var buf : [30000]u8 = undefined;

fn H(s: []const u8) u8 {
    var cv: u8 = 0;
    for (s) |c| {
        cv +%= c;
        cv *%= 17;
    }
    return cv;
}
const Lens = struct{lbl: []const u8, focal: u8};
const Box = std.ArrayList(Lens);

var boxes: [256]Box = undefined;

pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    for (&boxes) |*box| {box.* = try Box.initCapacity(alloc,3);} // we expect few collisions

    const input2 = input[0..std.mem.indexOfScalar(u8, input, '\n') orelse input.len];

    var part1: u64 = 0;
    var part2: u64 = 0;
    var comma_it = std.mem.splitScalar(u8, input2, ',');

    while(comma_it.next()) |part| {
        part1 += H(part);

        if (part[part.len-1]=='-') {
            const lbl = part[0..part.len-1];
            const h = H(lbl);

            for (0.., boxes[h].items) |i, lens| {
                if (std.mem.eql(u8, lbl, lens.lbl)) {_ = boxes[h].orderedRemove(i); break;}
            }
        } else if(part[part.len-2]=='=') {
            const lbl = part[0..part.len-2];
            const h = H(lbl);
            const focal = part[part.len-1]-'0';

            // replace or add
            for (boxes[h].items) |*lens| {
                if (std.mem.eql(u8, lbl, lens.lbl)) {lens.focal = focal; break;} //replace
            } else try boxes[h].append(Lens{.lbl=lbl, .focal=focal});
        } else unreachable;
    }
    //total up focusing power for part2
    for (1.., boxes) |i, box| {
        for (1.., box.items) |j, entry| {
            part2 += i * j * entry.focal;
        }
    }
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
