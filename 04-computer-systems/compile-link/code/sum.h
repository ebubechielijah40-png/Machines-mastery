#ifndef MM_SUM_H
#define MM_SUM_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
extern uint64_t successful_calls;
bool sum_bytes(const unsigned char *data, size_t length, uint64_t *output);
long affine(long x, long y); /* caller keeps 3*x+y within LONG range */
#endif
