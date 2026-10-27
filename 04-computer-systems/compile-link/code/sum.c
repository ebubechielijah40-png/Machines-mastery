#include "sum.h"
#include <stdint.h>
uint64_t successful_calls; /* zero initialized, external linkage */
bool sum_bytes(const unsigned char *data, size_t length, uint64_t *output) {
    if (output == NULL || (length != 0 && data == NULL)) return false;
    uint64_t total = 0;
    for (size_t i = 0; i < length; ++i) {
        if (UINT64_MAX - total < data[i]) return false;
        total += data[i];
    }
    *output = total; /* publish only after all checks */
    successful_calls += 1; /* uint64_t wraps; not a lifetime statistics service */
    return true;
}
long affine(long x, long y) { return 3*x + y; }
