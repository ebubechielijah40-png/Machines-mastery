def max_subarray_sum(values):
    if not values:
        raise ValueError("non-empty input required")
    ending=best=values[0]
    for i in range(1, len(values)):
        x = values[i]
        ending=max(x, ending+x)
        best=max(best, ending)
    return best
