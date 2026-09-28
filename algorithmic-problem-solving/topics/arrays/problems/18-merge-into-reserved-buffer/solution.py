def merge_into_buffer(a,m,b):
    if m<0 or m+len(b)!=len(a): raise ValueError("invalid lengths")
    i=m-1; j=len(b)-1; w=len(a)-1
    while j>=0:
        if i>=0 and a[i] > b[j]:
            a[w]=a[i]; i-=1
        else:
            a[w]=b[j]; j-=1
        w-=1
    return a
