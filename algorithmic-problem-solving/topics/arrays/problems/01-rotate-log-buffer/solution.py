def rotate_right(values, k):
    n=len(values)
    if n==0:
        return values
    k%=n
    if k==0:
        return values
    def rev(lo,hi):
        while lo<hi:
            values[lo],values[hi]=values[hi],values[lo]
            lo+=1; hi-=1
    rev(0,n-1); rev(0,k-1); rev(k,n-1)
    return values
