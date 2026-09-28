#include "../solutions/parser.h"
#include <assert.h>
#include <stdio.h>
int main(void)
{
    unsigned char b[3] = {0x12u, 0x34u, 0xFFu};
    unsigned int out = 999u;
    assert(read_be16(b, 3u, &out) == 1 && out == 4660u);
    for (unsigned int value = 0u; value < 65536u; ++value) {
        b[0] = (unsigned char)(value / 256u);
        b[1] = (unsigned char)(value % 256u);
        out = 999u;
        assert(read_be16(b, 2u, &out) == 1 && out == value);
    }
    out = 777u;
    assert(read_be16(NULL, 2u, &out) == 0 && out == 777u);
    assert(read_be16(b, 0u, &out) == 0 && out == 777u);
    assert(read_be16(b, 1u, &out) == 0 && out == 777u);
    assert(read_be16(b, 2u, NULL) == 0);
    assert(read_be16(NULL, 0u, NULL) == 0);
    puts("PASS: 65536 values, extra input, nulls, short lengths and unchanged output");
    return 0;
}
