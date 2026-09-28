def apply_range_deltas(n, updates):
    if n<0: raise ValueError("n must be nonnegative")
    diff=[0]*(n+1)
    for start,end,delta in updates:
        if not (0<=start<=end<n): raise ValueError("invalid range")
        diff[start]+=delta
        if end+1<n: diff[end+1]-=delta
    out=[]; cur=0
    for i in range(n):
        cur+=diff[i]; out.append(cur)
    return out
