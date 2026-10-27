#include "sum.h"
#include <inttypes.h>
#include <stdio.h>
int main(void) {
    const unsigned char sample[] = {3, 5, 7};
    uint64_t total = 999;
    if (!sum_bytes(sample, sizeof sample, &total)) return 1;
    printf("sum=%" PRIu64 " calls=%" PRIu64 " affine=%ld\n", total, successful_calls, affine(4, 5));
    return 0;
}
