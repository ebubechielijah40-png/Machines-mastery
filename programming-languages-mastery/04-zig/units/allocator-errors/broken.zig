const std = @import("std");
fn missingCleanup(allocator: std.mem.Allocator) !void {
    const first = try allocator.dupe(u8, "tag");
    const second = try allocator.dupe(u8, "DATA");
    allocator.free(second);
    allocator.free(first);
}
test "negative control detects missing error-path cleanup" {
    try std.testing.checkAllAllocationFailures(std.testing.allocator, missingCleanup, .{});
}
