#include "sum.h"
#include <assert.h>
#include <stdint.h>
int main(void) {
    uint64_t output = 123;
    assert(!sum_bytes(NULL, 1, &output) && output == 123);
    assert(!sum_bytes(NULL, 0, NULL));
    assert(sum_bytes(NULL, 0, &output) && output == 0);
    unsigned char data[256];
    for (size_t i=0; i<sizeof data; ++i) data[i]=(unsigned char)i;
    assert(sum_bytes(data,sizeof data,&output) && output == 32640);
    assert(successful_calls == 2);
    for(long x=-100;x<=100;++x)
        for(long y=-100;y<=100;++y) assert(affine(x,y)==x+x+x+y);
    return 0;
}
