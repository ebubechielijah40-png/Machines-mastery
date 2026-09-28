def first_missing_positive(values):
    n=len(values); i=0
    while i<n:
        v=values[i]
        if 1<=v<=n and values[v-1] != v:
            values[i],values[v-1]=values[v-1],values[i]
        else:
            i+=1
    for i,v in enumerate(values):
        if v != i+1:
            return i+1
    return n+1
