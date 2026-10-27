#include "arena.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
static unsigned random_state=17;
static unsigned next_random(void){random_state=random_state*1664525u+1013904223u;return random_state;}
int main(void){
 struct Arena a;arena_init(&a);assert(arena_check(&a));
 assert(!arena_alloc(&a,0));assert(!arena_alloc(&a,257));assert(!arena_alloc(&a,SIZE_MAX));
 unsigned char *p=arena_alloc(&a,7),*q=arena_alloc(&a,9);
 assert(p==a.bytes && q==a.bytes+8);assert(a.blocks[0].size==8 && a.blocks[1].size==16);
 assert(!arena_free(&a,p+1));assert(!arena_free(&a,NULL));
 assert(arena_free(&a,p));assert(!arena_free(&a,p));assert(arena_free(&a,q));
 assert(a.count==1 && a.blocks[0].size==256 && arena_check(&a));
 void *slots[32];for(size_t i=0;i<32;++i){slots[i]=arena_alloc(&a,8);assert(slots[i]);}
 for(size_t i=0;i<32;i+=2)assert(arena_free(&a,slots[i]));
 assert(!arena_alloc(&a,16)); /* 128 bytes free, no contiguous 16-byte interval */
 for(size_t i=1;i<32;i+=2)assert(arena_free(&a,slots[i]));
 assert(a.count==1 && arena_alloc(&a,256));
 arena_init(&a);
 unsigned char *live[16]={0};size_t lengths[16]={0};unsigned char tags[16]={0};
 for(size_t step=0;step<5000;++step){
  size_t s=next_random()%16;
  if(live[s]){assert(arena_free(&a,live[s]));live[s]=NULL;}
  else{size_t n=1+next_random()%40;unsigned char *got=arena_alloc(&a,n);if(got){live[s]=got;lengths[s]=n;tags[s]=(unsigned char)(s+1);memset(got,tags[s],n);}}
  assert(arena_check(&a));
  for(size_t i=0;i<16;++i)if(live[i])for(size_t k=0;k<lengths[i];++k)assert(live[i][k]==tags[i]);
  /* Independent live-allocation oracle, without consulting block metadata. */
  for(size_t i=0;i<16;++i)if(live[i]){
   size_t start=(size_t)(live[i]-a.bytes), reserved=(lengths[i]+7)/8*8;
   assert(start%8==0 && start+reserved<=256);
   for(size_t j=i+1;j<16;++j)if(live[j]){
    size_t other=(size_t)(live[j]-a.bytes), other_reserved=(lengths[j]+7)/8*8;
    assert(start+reserved<=other || other+other_reserved<=start);
   }
  }
 }
 puts("arena: boundary/coalescing/fragmentation and 5000 trace steps passed");
 return 0;
}
