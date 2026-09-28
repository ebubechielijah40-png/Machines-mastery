def next_permutation(values):
    n=len(values)
    if n<2:
        return False
    i=n-2
    while i>=0 and values[i] >= values[i+1]:
        i-=1
    if i<0:
        values.reverse(); return False
    j=n-1
    while values[j] <= values[i]:
        j-=1
    values[i],values[j]=values[j],values[i]
    values[i+1:]=reversed(values[i+1:])
    return True
