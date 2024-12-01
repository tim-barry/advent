
const std = @import("std");

const input = @embedFile("input02.txt");

const Bag = struct {
    red: u8,
    green: u8,
    blue: u8,
    fn union_with(self: *Bag, other: Bag) void {
        self.red = @max(self.red, other.red);
        self.green = @max(self.green, other.green);
        self.blue = @max(self.blue, other.blue);
    }
    fn contains(self: Bag, other: Bag) bool {
        return (self.red >= other.red) and (self.green >= other.green) and (self.blue >= other.blue);
    }
    fn power(self: Bag) u32 {
        return @as(u32, self.red)*@as(u32, self.green) * @as(u32, self.blue);
    }
};

const goal_bag = Bag{.red = 12, .green = 13, .blue = 14};

const Game = struct {
    id: u8,
    pulls: std.ArrayList(Bag),
    fn id_if_possible(self: Game) u8 {
        return lbl: for (self.pulls.items) |pull| {
            if (!goal_bag.contains(pull)) break :lbl 0;
        } else self.id;
    }
    fn min_bag(self: Game) Bag {
        var bag = Bag{.red=0, .green=0, .blue=0};
        // mutates
        for (self.pulls.items) |pull| {
            bag.union_with(pull);
        }
        return bag;
    }
};
var buf: [1000]u8 = undefined;

pub fn main() !void {
    var part1: u32 = 0;
    var part2: u32 = 0;
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const alloc = fba.allocator();

    var lines = std.mem.splitScalar(u8, input, '\n');
    while (lines.next()) |line| {
        if (line.len==0) continue;
        var game: Game = undefined;
        game.pulls = std.ArrayList(Bag).init(alloc);
        defer game.pulls.deinit();
        var colon_it = std.mem.splitScalar(u8, line, ':');
        const game_id = colon_it.next().?;
        game.id = try std.fmt.parseInt(u8, game_id[5..], 10);

        const rest_of_line = colon_it.next().?;
        var pulls = std.mem.splitScalar(u8, rest_of_line, ';');
        while (pulls.next()) |pull| {
            var p: Bag = .{.red = 0, .green = 0, .blue = 0};
            var cubes = std.mem.splitScalar(u8, pull, ',');
            while (cubes.next()) |cube| {
                var cube_it = std.mem.splitScalar(u8, cube[1..], ' ');
                const n = try std.fmt.parseInt(u8, cube_it.next().?, 10);
                const str = cube_it.next().?;
                if (std.mem.eql(u8,str,"red")) {p.red = n;}
                if (std.mem.eql(u8,str,"green")) {p.green = n;}
                if (std.mem.eql(u8,str,"blue")) {p.blue = n;}
            }
            try game.pulls.append(p);
        }
        part1 += game.id_if_possible();
        part2 += game.min_bag().power();
    }
    const stdout = std.io.getStdOut().writer();
    try stdout.print("{}\n{}\n", .{part1, part2});
}

