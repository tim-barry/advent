const std = @import("std");
const Vector = std.meta.Vector;
const parseInt = std.fmt.parseInt;

const input = @embedFile("input.txt");

const I = i8;
const useVector = true; // both work
const P = if (useVector) Vector(3, I) else struct {
    x: I,
    y: I,
    z: I,
};

const Dir = if (useVector) P else u3;

const dirs: [6]Dir = if (useVector)
.{
    .{ 1, 0, 0 },
    .{ -1, 0, 0 },
    .{ 0, 1, 0 },
    .{ 0, -1, 0 },
    .{ 0, 0, 1 },
    .{ 0, 0, -1 },
} else .{ 0, 1, 2, 3, 4, 5 };

fn move(p: P, comptime d: Dir) P {
    if (useVector) {
        return p + d;
    } else {
        const neg: comptime_int = if (d % 2 == 0) 1 else -1;
        return P{
            .x = p.x + (if (d / 2 == 0) 1 else 0) * neg,
            .y = p.y + (if (d / 2 == 1) 1 else 0) * neg,
            .z = p.z + (if (d / 2 == 2) 1 else 0) * neg,
        };
    }
}

const PSet = std.AutoHashMap(P, void);

fn makeP(txt: []const u8) !P {
    var it = std.mem.split(u8, txt, ",");
    const x = try parseInt(I, it.next() orelse return error.NoInput, 10);
    const y = try parseInt(I, it.next() orelse return error.NoInput, 10);
    const z = try parseInt(I, it.next() orelse return error.NoInput, 10);
    if (useVector) {
        return .{ x, y, z };
    } else {
        return .{ .x = x, .y = y, .z = z };
    }
}

fn surface(data: PSet) u32 {
    var tot: u32 = 0;
    var it = data.keyIterator();
    while (it.next()) |p| {
        inline for (dirs) |d| {
            tot += if (data.contains(move(p.*, d))) 0 else 1;
        }
    }
    return tot;
}

fn part1(data: PSet) u32 {
    return surface(data);
}

fn part2(data: PSet, allocator: std.mem.Allocator) !u32 {
    if (useVector) {
        var total = PSet.init(allocator);
        var mins: P = P{ 30, 30, 30 };
        var maxs: P = P{ -1, -1, -1 };
        var it = data.keyIterator();
        while (it.next()) |p| {
            mins = @min(mins, p.*);
            maxs = @max(maxs, p.*);
        }
        mins -= P{ 1, 1, 1 };
        maxs += P{ 1, 1, 1 };
        var x: I = mins[0];
        while (x <= maxs[0]) : (x += 1) {
            var y: I = mins[1];
            while (y <= maxs[1]) : (y += 1) {
                var z: I = mins[2];
                while (z <= maxs[2]) : (z += 1) {
                    //const p = P{x,y,z};
                    try total.putNoClobber(P{ x, y, z }, {});
                }
            }
        }
        // setup outside/total: floodfill outside air from min
        var out = PSet.init(allocator); // visited
        var q1 = PSet.init(allocator);
        var q2 = PSet.init(allocator);
        try q1.putNoClobber(mins, {});
        while (q1.count() > 0) {
            var q1it = q1.keyIterator();
            while (q1it.next()) |p| {
                try out.putNoClobber(p.*, {});
                inline for (dirs) |d| {
                    const m = move(p.*, d);
                    if (total.contains(m) and !(out.contains(m) or data.contains(m))) try q2.put(m, {});
                }
            }
            var tmp = q1;
            q1 = q2;
            q2 = tmp;
            q2.clearRetainingCapacity();
        }
        // remove outer air from total
        var outit = out.keyIterator();
        while (outit.next()) |p| {
            _ = total.remove(p.*);
        }
        return surface(total);
    } else return 0;
}

pub fn main() !void {
    // parse input
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    //defer _ = gpa.deinit();
    const alloc = gpa.allocator();
    const data = initDroplet: {
        var tmp = PSet.init(alloc);
        const desiredCapacity = @intCast(u32, std.mem.count(u8, input, "\n"));
        try tmp.ensureTotalCapacity(desiredCapacity);
        var it = std.mem.split(u8, input, "\n");
        while (it.next()) |line| {
            if (line.len == 0) break;
            tmp.putAssumeCapacityNoClobber(try makeP(line), {});
        }
        break :initDroplet tmp;
    };
    //defer data.deinit(); // data must be non-const
    std.debug.print("part 1: {}\n", .{part1(data)});
    std.debug.print("part 1: {}\n", .{try part2(data, alloc)});
}
