#ifndef MM_PARSER_H
#define MM_PARSER_H
#include <stddef.h>
int read_be16(const unsigned char *p, size_t n, unsigned int *out);
#endif
