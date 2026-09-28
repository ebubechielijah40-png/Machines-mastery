def run_length_encode(values):
    if not values:
        return []
    out=[]; cur=values[0]; count=1
    for x in values[1:]:
        if x==cur:
            count+=1
        else:
            out.append((cur,count)); cur=x; count=1
    out.append((cur,count))
    return out
