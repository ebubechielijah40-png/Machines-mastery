"""Original exact integer invariant examples, not constant-time cryptography."""


def integer(x):
    if type(x) is not int:raise ValueError('expected an integer, not bool')
    return x


def extended_gcd(a,b):
    a,b=integer(a),integer(b)
    old_r,r=abs(a),abs(b)
    old_s,s=1,0;old_t,t=0,1
    while r:
        quotient=old_r//r
        old_r,r=r,old_r-quotient*r
        old_s,s=s,old_s-quotient*s
        old_t,t=t,old_t-quotient*t
    return old_r,old_s*(-1 if a<0 else 1),old_t*(-1 if b<0 else 1)


def modular_power(base,exponent,modulus):
    base,exponent,modulus=map(integer,(base,exponent,modulus))
    if exponent<0 or modulus<=0:raise ValueError('nonnegative exponent and positive modulus required')
    result=1%modulus;base%=modulus
    while exponent:
        if exponent%2:result=result*base%modulus
        base=base*base%modulus;exponent//=2
    return result


def page_count(byte_count,page_size):
    n,p=integer(byte_count),integer(page_size)
    if n<0 or p<=0:raise ValueError('nonnegative size and positive page capacity required')
    return n//p+int(n%p!=0)
