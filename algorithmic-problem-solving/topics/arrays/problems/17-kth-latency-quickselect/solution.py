def kth_smallest(values,k):
    if not 0<=k<len(values): raise IndexError("k out of range")
    lo=0; hi=len(values)-1
    while True:
        pivot=values[hi]; p=lo
        for i in range(lo,hi):
            if values[i] <= pivot:
                values[p],values[i]=values[i],values[p]; p+=1
        values[p],values[hi]=values[hi],values[p]
        if p==k: return values[p]
        if p<k: lo=p+1
        else: hi=p-1
