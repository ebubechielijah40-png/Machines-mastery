def max_subarray_sum(values):
    if not values:
        raise ValueError("non-empty input required")
    ending=best=values[0]
    for x in values[1:]:
        ending=max(x, ending+x)
        best=max(best, ending)
    return best
