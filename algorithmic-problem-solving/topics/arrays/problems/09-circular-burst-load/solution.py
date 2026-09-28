def max_circular_subarray_sum(values):
    if not values:
        raise ValueError("non-empty input required")
    total=sum(values)
    max_end=max_all=values[0]
    min_end=min_all=values[0]
    for x in values[1:]:
        max_end=max(x,max_end+x); max_all=max(max_all,max_end)
        min_end=min(x,min_end+x); min_all=min(min_all,min_end)
    if max_all < 0:
        return max_all
    return max(max_all,total-min_all)
