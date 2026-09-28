def product_except_self(values):
    n=len(values); out=[1]*n
    p=1
    for i,x in enumerate(values):
        out[i]=p; p*=x
    s=1
    for i in range(n-1,-1,-1):
        out[i]*=s; s*=values[i]
    return out
