#include "arena.h"
void arena_init(struct Arena *a) {
    a->count=1; a->blocks[0]=(struct Block){0,ARENA_CAPACITY,false};
}
bool arena_check(const struct Arena *a) {
    if(a->count<1 || a->count>ARENA_BLOCKS) return false;
    size_t end=0;
    for(size_t i=0;i<a->count;++i) {
        struct Block b=a->blocks[i];
        if(b.offset!=end || !b.size || b.size%ARENA_ALIGNMENT || b.size>ARENA_CAPACITY-end) return false;
        if(i && !b.used && !a->blocks[i-1].used) return false;
        end+=b.size;
    }
    return end==ARENA_CAPACITY;
}
void *arena_alloc(struct Arena *a,size_t requested) {
    if(!requested || requested>ARENA_CAPACITY) return NULL;
    size_t rounded=(requested+ARENA_ALIGNMENT-1)/ARENA_ALIGNMENT*ARENA_ALIGNMENT;
    for(size_t i=0;i<a->count;++i) {
        struct Block *b=&a->blocks[i];
        if(b->used || b->size<rounded) continue;
        size_t remainder=b->size-rounded;
        if(remainder && a->count==ARENA_BLOCKS) return NULL;
        if(remainder) {
            for(size_t j=a->count;j>i+1;--j) a->blocks[j]=a->blocks[j-1];
            a->blocks[i+1]=(struct Block){b->offset+rounded,remainder,false};
            a->count++;b->size=rounded;
        }
        b->used=true;return a->bytes+b->offset;
    }
    return NULL;
}
bool arena_free(struct Arena *a,void *pointer) {
    for(size_t i=0;i<a->count;++i) {
        struct Block *b=&a->blocks[i];
        /* Equality is checked without subtracting an unrelated pointer. */
        if(pointer!=(void *)(a->bytes+b->offset)) continue;
        if(!b->used) return false;
        b->used=false;
        for(size_t j=0;j+1<a->count;) {
            if(!a->blocks[j].used && !a->blocks[j+1].used) {
                a->blocks[j].size+=a->blocks[j+1].size;
                for(size_t k=j+1;k+1<a->count;++k) a->blocks[k]=a->blocks[k+1];
                a->count--;
            } else j++;
        }
        return true;
    }
    return false;
}
