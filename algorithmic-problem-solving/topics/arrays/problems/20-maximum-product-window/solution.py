def max_product_subarray(values):
    if not values: raise ValueError("non-empty input required")
    hi=lo=best=values[0]
    for i in range(1, len(values)):
        x = values[i]
        if x<0: hi,lo=lo,hi
        hi=max(x,hi*x)
        lo=min(x,lo*x)
        best=max(best,hi)
    return best
