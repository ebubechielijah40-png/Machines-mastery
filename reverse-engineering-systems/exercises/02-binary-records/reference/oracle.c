/* Original controlled teaching oracle, not an upstream protocol implementation. */
#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int number(const char *s, long lo, long hi, long *out) {
    char *end;
    errno = 0;
    if (*s == '\0' || *s == ' ' || *s == '\t' || *s == '\n') return 0;
    long n = strtol(s, &end, 10);
    if (errno || *end || n < lo || n > hi) return 0;
    *out = n;
    return 1;
}
static int nibble(char c) {
    if (c >= '0' && c <= '9') return c-'0';
    if (c >= 'a' && c <= 'f') return c-'a'+10;
    if (c >= 'A' && c <= 'F') return c-'A'+10;
    return -1;
}
static uint16_t crc(const unsigned char *p, size_t count) {
    uint16_t value = UINT16_C(0xffff);
    for (size_t i = 0; i < count; ++i) {
        value ^= (uint16_t)((uint16_t)p[i] << 8);
        for (int bit = 0; bit < 8; ++bit)
            value = (uint16_t)((value & UINT16_C(0x8000)) ?
                     ((uint32_t)value << 1) ^ UINT32_C(0x1021) : (uint32_t)value << 1);
    }
    return value;
}
int main(int argc, char **argv) {
    long sequence, sample, enabled;
    if (argc != 5 || !number(argv[1],0,65535,&sequence) ||
        !number(argv[2],-32768,32767,&sample) || !number(argv[3],0,1,&enabled)) return 2;
    size_t length = strlen(argv[4]);
    if (length > 64 || length % 2) return 2;
    length /= 2;
    unsigned char packet[44] = {0x4d,0x58,1,0,0,0,0,0,0,0};
    packet[3] = (unsigned char)enabled;
    packet[4] = (unsigned char)((unsigned long)sequence & 255UL);
    packet[5] = (unsigned char)((unsigned long)sequence >> 8);
    uint16_t word = (uint16_t)sample; /* modulo 2^16; no host signed representation copied */
    packet[6] = (unsigned char)(word >> 8);
    packet[7] = (unsigned char)(word & UINT16_C(255));
    packet[8] = (unsigned char)length;
    packet[9] = 0;
    for (size_t i = 0; i < length; ++i) {
        int a = nibble(argv[4][2*i]), b = nibble(argv[4][2*i+1]);
        if (a < 0 || b < 0) return 2;
        packet[10+i] = (unsigned char)(16*a+b);
    }
    uint16_t check = crc(packet,10+length);
    packet[10+length] = (unsigned char)(check >> 8);
    packet[11+length] = (unsigned char)(check & UINT16_C(255));
    for (size_t i = 0; i < 12+length; ++i) printf("%02x",(unsigned int)packet[i]);
    putchar('\n');
    return 0;
}
