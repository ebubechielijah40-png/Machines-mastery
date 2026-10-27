#include "arena.h"
#include <assert.h>
#include <stdio.h>

static void snapshot(const char *name, const struct Arena *arena) {
    size_t free_total = 0, largest = 0;
    printf("{\"name\":\"%s\",\"blocks\":[", name);
    for (size_t i = 0; i < arena->count; ++i) {
        struct Block block = arena->blocks[i];
        printf("%s{\"offset\":%zu,\"size\":%zu,\"used\":%s}",
               i ? "," : "", block.offset, block.size,
               block.used ? "true" : "false");
        if (!block.used) {
            free_total += block.size;
            if (block.size > largest) largest = block.size;
        }
    }
    printf("],\"free_total\":%zu,\"largest_hole\":%zu}", free_total, largest);
}

int main(void) {
    struct Arena arena;
    arena_init(&arena);
    printf("{\"arena_size\":%zu,\"block_size\":%zu,\"snapshots\":[",
           sizeof arena, sizeof(struct Block));
    snapshot("initial", &arena);
    void *first = arena_alloc(&arena, 7), *second = arena_alloc(&arena, 9);
    assert(first && second && arena_check(&arena));
    printf(","); snapshot("requests_7_9", &arena);
    assert(arena_free(&arena, first) && arena_free(&arena, second));
    void *slots[32];
    for (size_t i = 0; i < 32; ++i) {
        slots[i] = arena_alloc(&arena, 8); assert(slots[i]);
    }
    for (size_t i = 0; i < 32; i += 2) assert(arena_free(&arena, slots[i]));
    printf(","); snapshot("alternating_holes", &arena);
    bool rejected = arena_alloc(&arena, 16) == NULL;
    assert(rejected && arena_check(&arena));
    for (size_t i = 1; i < 32; i += 2) assert(arena_free(&arena, slots[i]));
    printf(","); snapshot("coalesced", &arena);
    printf("],\"request_16_rejected\":%s}\n", rejected ? "true" : "false");
    return 0;
}
