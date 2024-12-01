
const std = @import("std");

const Pos = i16;

const input = @embedFile("input.txt");
const W = std.mem.indexOfScalar(u8, input, '\n').?;
const lW: Pos = @intCast(W+1);
const H = @divExact(input.len, lW);

var buf : [1000000]u8 = undefined;

const Direction = enum(Pos) {
    right = 1,
    down = lW,
    left = -1,
    up = -lW,
};
const State = struct {
    pos: Pos,
    dir: Direction,
};

inline fn valid(p: Pos) bool {
    return (p > 0) and (p < input.len) and (input[@intCast(p)] != '\n');
}

fn appendUnique(nodes: *std.ArrayList(State), state: State) !void {
    for (nodes.items) |it| if (it.pos==state.pos and it.dir==state.dir) return;
    try nodes.append(state);
}

fn energized(alloc: std.mem.Allocator, start: State) !u32 {
    // var visited = std.AutoHashMap(State).init(alloc);
    var visited = std.AutoHashMap(Pos, [4]?Direction).init(alloc);
    defer visited.deinit();
    var nodes = std.ArrayList(State).init(alloc);
    defer nodes.deinit();
    try nodes.append(start);
    // we don't really care about iteration order
    loop: while (nodes.items.len > 0) {
        const here = nodes.pop();
        // if (visited.contains(here)) continue :loop;
        // try visited.put(here, {});
        if (visited.getPtr(here.pos)) |dirs| {
            inline for (dirs) |*dir| {
                if (dir.*==here.dir) continue :loop;
                if (dir.*==null) {dir.* = here.dir; break;}
            }
        } else {
            try visited.put(here.pos, [4]?Direction{here.dir, null, null, null});
        }
        switch (input[@intCast(here.pos)]) {
            '.' => {
                const np = here.pos + @intFromEnum(here.dir);
                if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=here.dir});
            },
            '|' => switch(here.dir) {
                .up, .down => {
                    const np = here.pos + @intFromEnum(here.dir);
                    if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=here.dir});
                },
                .left, .right => for ([2]Direction{.up, .down}) |dp| {
                    const np = here.pos + @intFromEnum(dp);
                    if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=dp});
                },
            },
            '-' => switch(here.dir) {
                .left, .right => {
                    const np = here.pos + @intFromEnum(here.dir);
                    if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=here.dir});
                },
                .up, .down => for ([2]Direction{.left, .right}) |dp| {
                    const np = here.pos + @intFromEnum(dp);
                    if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=dp});
                },
            },
            '/' => {
                const dp: Direction = switch (here.dir) {
                    .up => .right, .right => .up, .left => .down, .down => .left,
                };
                const np = here.pos + @intFromEnum(dp);
                if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=dp});
            },
            '\\' => {
                const dp: Direction = switch (here.dir) {
                    .up => .left, .left => .up, .right => .down, .down => .right,
                };
                const np = here.pos + @intFromEnum(dp);
                if (valid(np)) try appendUnique(&nodes, .{.pos=np, .dir=dp});
            },
            else => unreachable,
        }
    }
    // while (visited.)
    return visited.count();
}


pub fn main() !void {
    const w = std.io.getStdOut().writer();
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var part1: u32 = try energized(alloc, .{.pos=0, .dir=.right});
    var part2: u32 = 0;
    //topdown, bottomup
    for (0..W) |x| {
        fba.reset();
        const topdown = try energized(alloc, .{.pos=@intCast(x), .dir=.down});
        if (topdown > part2) part2 = topdown;
        fba.reset();
        const bottomup = try energized(alloc, .{.pos=@intCast(x + (H-1)*lW), .dir=.up});
        if (bottomup > part2) part2 = bottomup;
    }
    for (0..H) |y| {
        fba.reset();
        const left = try energized(alloc, .{.pos=@intCast(y*lW), .dir=.right});
        if (left > part2) part2 = left;
        fba.reset();
        const right = try energized(alloc, .{.pos=@intCast((W-1) + y*lW), .dir=.left});
        if (right > part2) part2 = right;
    }
    //
    try w.print("part1: {}\npart2: {}\n", .{part1, part2});
}
