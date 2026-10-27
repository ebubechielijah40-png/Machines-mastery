#include <errno.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

extern uint64_t weighted8(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
extern unsigned entry_alignment(void);
extern unsigned check_good(void),check_bad(void);
extern long raw_getpid(void),raw_write(long,const void *,unsigned long);
volatile unsigned char zero_area[8192];
struct Row { unsigned char kind; uint64_t value; unsigned short code; };

int main(void) {
    unsigned zero_sum=0;
    for(size_t i=0;i<sizeof zero_area;i++) zero_sum+=zero_area[i];
    unsigned cases=0;
    for(uint64_t k=0;k<100;k++) {
        uint64_t expected=0;
        for(uint64_t i=1;i<=8;i++) expected+=i*(k+i);
        if(weighted8(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8)!=expected) return 2;
        cases++;
    }
    long raw=raw_write(-1,"",0);
    errno=0;
    long wrapped=write(-1,"",0);
    int error=errno;
    printf("{\"weighted_cases\":%u,\"weighted_1_to_8\":%" PRIu64 ",\"entry_alignment\":%u,\"good_preserves\":%u,\"mutant_preserves\":%u,\"pid_equal\":%d,\"raw_write\":%ld,\"libc_write\":%ld,\"libc_errno\":%d,\"bss_zero_sum\":%u,\"row_size\":%zu,\"row_align\":%zu,\"value_offset\":%zu,\"code_offset\":%zu}\n",
           cases,weighted8(1,2,3,4,5,6,7,8),entry_alignment(),check_good(),check_bad(),
           raw_getpid()==(long)getpid(),raw,wrapped,error,zero_sum,sizeof(struct Row),
           _Alignof(struct Row),offsetof(struct Row,value),offsetof(struct Row,code));
    return 0;
}
