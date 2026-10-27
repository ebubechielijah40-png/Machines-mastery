#ifndef MM_ARENA_H
#define MM_ARENA_H
#include <stdbool.h>
#include <stddef.h>
#define ARENA_CAPACITY 256
#define ARENA_BLOCKS 64
#define ARENA_ALIGNMENT 8
struct Block { size_t offset, size; bool used; };
struct Arena { _Alignas(8) unsigned char bytes[ARENA_CAPACITY]; struct Block blocks[ARENA_BLOCKS]; size_t count; };
void arena_init(struct Arena *a);
void *arena_alloc(struct Arena *a, size_t requested);
bool arena_free(struct Arena *a, void *pointer);
bool arena_check(const struct Arena *a);
#endif
