const std = @import("std");
const Allocator = std.mem.Allocator;

pub const Packet = struct {
    allocator: Allocator,
    tag: []u8,
    body: []u8,

    pub fn init(allocator: Allocator, tag: []const u8, body: []const u8) !Packet {
        if (tag.len == 0 or tag.len > 32) return error.BadTag;
        if (body.len > 4096) return error.BodyTooLong;
        const owned_tag = try allocator.dupe(u8, tag);
        errdefer allocator.free(owned_tag);
        const owned_body = try allocator.dupe(u8, body);
        return .{ .allocator = allocator, .tag = owned_tag, .body = owned_body };
    }
    pub fn deinit(self: *Packet) void {
        self.allocator.free(self.body);
        self.allocator.free(self.tag);
        self.* = undefined;
    }
};

fn allocationScenario(allocator: Allocator) !void {
    var packet = try Packet.init(allocator, "msg", "payload");
    defer packet.deinit();
    try std.testing.expectEqualStrings("payload", packet.body);
}

test "caller bytes and owned bytes evolve independently" {
    var tag = [_]u8{ 'h', 'd', 'r' };
    var body = [_]u8{ 1, 2, 3 };
    var packet = try Packet.init(std.testing.allocator, &tag, &body);
    defer packet.deinit();
    tag[0] = 'x'; body[0] = 9;
    try std.testing.expectEqualStrings("hdr", packet.tag);
    try std.testing.expectEqualSlices(u8, &[_]u8{ 1, 2, 3 }, packet.body);
    packet.body[1] = 8;
    try std.testing.expectEqual(@as(u8, 2), body[1]);
}
test "every allocation failure cleans previously acquired allocations" {
    try std.testing.checkAllAllocationFailures(std.testing.allocator, allocationScenario, .{});
}
test "second allocation failure rolls fixed u8 arena back to zero" {
    var buffer: [4]u8 = undefined;
    var fixed = std.heap.FixedBufferAllocator.init(&buffer);
    try std.testing.expectError(error.OutOfMemory, Packet.init(fixed.allocator(), "tag", "DATA"));
    try std.testing.expectEqual(@as(usize, 0), fixed.end_index);
}
test "reverse cleanup reclaims the two most recent byte allocations" {
    var buffer: [8]u8 = undefined;
    var fixed = std.heap.FixedBufferAllocator.init(&buffer);
    var packet = try Packet.init(fixed.allocator(), "tag", "DATA");
    try std.testing.expectEqual(@as(usize, 7), fixed.end_index);
    packet.deinit();
    try std.testing.expectEqual(@as(usize, 0), fixed.end_index);
}
test "invalid shape rejected before allocator use" {
    var buffer: [0]u8 = .{};
    var fixed = std.heap.FixedBufferAllocator.init(&buffer);
    try std.testing.expectError(error.BadTag, Packet.init(fixed.allocator(), "", "DATA"));
    try std.testing.expectError(error.BodyTooLong, Packet.init(fixed.allocator(), "tag", &([_]u8{0} ** 4097)));
    try std.testing.expectEqual(@as(usize, 0), fixed.end_index);
}
test "zero-length body still has single owned cleanup path" {
    var packet = try Packet.init(std.testing.allocator, "e", "");
    defer packet.deinit();
    try std.testing.expectEqual(@as(usize, 0), packet.body.len);
}

pub fn main() !void {
    inline for (.{ 1, 2, 4, 8, 16 }) |budget| {
        var buffer: [budget]u8 = undefined;
        var fixed = std.heap.FixedBufferAllocator.init(&buffer);
        if (Packet.init(fixed.allocator(), "tag", "DATA")) |owned| {
            var packet = owned;
            const used = fixed.end_index;
            packet.deinit();
            std.debug.print("budget={d};status=success;peak_byte_end={d};after_cleanup={d}\n", .{ budget, used, fixed.end_index });
        } else |err| {
            std.debug.print("budget={d};status={s};after_cleanup={d}\n", .{ budget, @errorName(err), fixed.end_index });
        }
    }
}
