def minimal_sort_window(values):
    n=len(values)
    if n<2:
        return (-1,-1)
    l=0
    while l<n-1 and values[l] <= values[l+1]: l+=1
    if l==n-1: return (-1,-1)
    r=n-1
    while r>0 and values[r-1] <= values[r]: r-=1
    wmin=min(values[l:r+1]); wmax=max(values[l:r+1])
    while l>0 and values[l-1] > wmin: l-=1
    while r<n-1 and values[r+1] < wmax: r+=1
    return (l,r)
