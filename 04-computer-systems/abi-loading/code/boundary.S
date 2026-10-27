#include <asm/unistd.h>
.text
.globl weighted8
.type weighted8,@function
weighted8:
    mov %rdi,%rax
    lea (%rax,%rsi,2),%rax
    lea (%rdx,%rdx,2),%r10
    add %r10,%rax
    lea (%rax,%rcx,4),%rax
    lea (%r8,%r8,4),%r10
    add %r10,%rax
    lea (%r9,%r9,2),%r10
    lea (%rax,%r10,2),%rax
    mov 8(%rsp),%r10
    imul $7,%r10,%r10
    add %r10,%rax
    mov 16(%rsp),%r10
    lea (%rax,%r10,8),%rax
    ret
.size weighted8,.-weighted8

.globl entry_alignment
.type entry_alignment,@function
entry_alignment:
    lea 8(%rsp),%rax
    and $15,%eax
    ret
.size entry_alignment,.-entry_alignment

.type touch_good,@function
touch_good:
    push %rbx
    mov $9,%ebx
    pop %rbx
    ret
.size touch_good,.-touch_good
.type touch_bad,@function
touch_bad:
    mov $9,%ebx
    ret
.size touch_bad,.-touch_bad

.macro checker name,target
.globl \name
.type \name,@function
\name:
    push %rbx
    mov $12345,%ebx
    call \target
    cmp $12345,%rbx
    sete %al
    movzbl %al,%eax
    pop %rbx
    ret
.size \name,.-\name
.endm
checker check_good,touch_good
checker check_bad,touch_bad

.globl raw_getpid
.type raw_getpid,@function
raw_getpid:
    mov $__NR_getpid,%eax
    syscall
    ret
.size raw_getpid,.-raw_getpid
.globl raw_write
.type raw_write,@function
raw_write:
    mov $__NR_write,%eax
    syscall
    ret
.size raw_write,.-raw_write
.section .note.GNU-stack,"",@progbits
