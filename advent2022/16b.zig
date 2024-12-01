const std = @import("std");

//AA=0
//'AA', 'AI', 'AQ', 'AZ', 'HA', 'HC', 'IM', 'IY', 'KQ', 'KZ', 'LS', 'QK', 'RF', 'VI', 'YC', 'ZJ'
//
const Pos: type = u64;
const Score: type = i64;
const Idx: type = u32;
const Cost: type = i64;

const cost = [16][16]Cost{ // Distance array
    [16]Cost{ 1, 7, 12, 8, 10, 7, 13, 10, 3, 4, 5, 3, 6, 10, 6, 3 },
    [16]Cost{ 8, 1, 16, 12, 14, 5, 17, 14, 10, 7, 9, 5, 10, 14, 3, 7 },
    [16]Cost{ 13, 16, 1, 5, 3, 16, 5, 3, 10, 10, 12, 12, 7, 7, 14, 13 },
    [16]Cost{ 9, 12, 5, 1, 3, 12, 6, 3, 6, 6, 8, 8, 3, 3, 10, 9 },
    [16]Cost{ 11, 14, 3, 3, 1, 14, 5, 3, 8, 8, 10, 10, 5, 4, 12, 11 },
    [16]Cost{ 8, 5, 16, 12, 14, 1, 17, 14, 10, 7, 9, 5, 10, 14, 3, 7 },
    [16]Cost{ 13, 16, 5, 6, 4, 16, 1, 3, 10, 10, 12, 12, 8, 4, 14, 13 },
    [16]Cost{ 11, 14, 3, 3, 3, 14, 3, 1, 8, 8, 10, 10, 5, 4, 12, 11 },
    [16]Cost{ 3, 9, 10, 6, 8, 9, 11, 8, 1, 5, 3, 5, 4, 8, 8, 5 },
    [16]Cost{ 4, 7, 10, 6, 8, 7, 11, 8, 6, 1, 3, 3, 4, 8, 5, 4 },
    [16]Cost{ 4, 8, 12, 8, 10, 8, 13, 10, 3, 3, 1, 4, 6, 10, 7, 4 },
    [16]Cost{ 3, 5, 12, 8, 10, 5, 13, 10, 6, 3, 5, 1, 6, 10, 3, 3 },
    [16]Cost{ 6, 10, 7, 3, 5, 10, 8, 5, 4, 4, 6, 6, 1, 5, 8, 7 },
    [16]Cost{ 11, 14, 7, 3, 4, 14, 4, 4, 8, 8, 10, 10, 5, 1, 12, 11 },
    [16]Cost{ 6, 3, 14, 10, 12, 3, 15, 12, 8, 5, 7, 3, 8, 12, 1, 5 },
    [16]Cost{ 3, 6, 13, 9, 11, 6, 14, 11, 6, 4, 4, 3, 8, 11, 4, 1 },
};

const benefit = [16]Score{ 0, 25, 23, 20, 12, 24, 19, 15, 17, 5, 3, 10, 18, 22, 9, 6 };

inline fn swap(comptime T: type, a: *T, b: *T) void {
    const tmp = a.*;
    a.* = b.*;
    b.* = tmp;
}
pub const PermutationError = error{ListTooLong};

/// Returns an iterator that iterates all the permutations of `list`.
/// `permutate(u8, slice_of_bytes)`
/// will return all permutations of slice_of_bytes followed by `null` as the last value.
/// If `list.len` is greater than 16 an error is returned.
pub fn permutate(comptime T: type, list: []T) PermutationError!PermutationIterator(T) {
    if (list.len > 16) return PermutationError.ListTooLong;

    return PermutationIterator(T){
        .list = list[0..],
        .size = @intCast(u4, list.len),
        .state = [_]u4{0} ** 16,
        .stateIndex = 0,
        .first = true,
    };
}

pub fn PermutationIterator(comptime T: type) type {
    return struct {
        list: []T,
        size: u4,
        state: [16]u4,
        stateIndex: u4,
        first: bool,

        const Self = @This();

        pub fn next(self: *Self) ?[]T {
            if (self.first) {
                self.first = false;
                return self.list;
            }

            while (self.stateIndex < self.size) {
                if (self.state[self.stateIndex] < self.stateIndex) {
                    if (self.stateIndex % 2 == 0) {
                        swap(T, &self.list[0], &self.list[self.stateIndex]);
                    } else {
                        swap(T, &self.list[self.state[self.stateIndex]], &self.list[self.stateIndex]);
                    }

                    self.state[self.stateIndex] += 1;
                    self.stateIndex = 0;

                    return self.list;
                } else {
                    self.state[self.stateIndex] = 0;
                    self.stateIndex += 1;
                }
            }

            return null;
        }
    };
}

fn score(perm: []Pos, prevM: Score) Score {
    var split: Idx = 1;
    var mtot: Score = 0;
    var msplit: Idx = 0;
    //var splitOK: bool = true;
    //outer:
    outer: while (split < perm.len) : (split += 1) {
        var tot: Score = 0;
        var time: Score = 26;
        var j: Idx = 0;
        var pos: Pos = 0; // AA
        //for (perm[0..split]) |npos| {
        //}
        while (j < split) : (j += 1) {
            const npos: Pos = perm[j];
            time -= cost[pos][npos];
            if (time <= 0) {
                //splitOK = false;
                break :outer;
            }
            tot += time * benefit[npos];
            pos = npos;
        }
        pos = 0; // AA
        time = 26;
        while (j < perm.len) : (j += 1) {
            const npos: Pos = perm[j];
            time -= cost[pos][npos];
            if (time <= 0) {
                break;
            }
            tot += time * benefit[npos];
            pos = npos;
        }
        if (tot > mtot) {
            mtot = tot;
            msplit = split;
        }
    }
    if (mtot > prevM) {
        std.debug.print("score {} paths: {any}, {any}\n", .{ mtot, perm[0..msplit], perm[msplit..] });
        return mtot;
    }
    return prevM;
}

fn part2() !void {
    var nums = [_]Pos{ 8, 2, 3, 4, 5, 6, 7, 1, 9, 10, 11, 12, 13, 14, 15 };
    var it = try permutate(Pos, nums[1..]); // 14!
    var max: Score = 0;
    while (it.next()) |unused| {
        _ = unused;
        max = score(nums[0..], max);
    }
    //std.debug.print("{}\n",);
}

pub fn main() !void {
    try part2();
}
