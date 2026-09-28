#include "parser.h"
#include <limits.h>
_Static_assert(CHAR_BIT == 8, "This format requires eight-bit bytes");
_Static_assert(UINT_MAX >= 65535u, "Result needs at least sixteen value bits");
int read_be16(const unsigned char *p, size_t n, unsigned int *out)
{
    if (p == NULL || out == NULL || n < 2u) {
        return 0;
    }
    *out = (unsigned int)p[0] * 256u + (unsigned int)p[1];
    return 1;
}
