"""Original logical payload-budget example; this is not Python heap accounting."""

def choose_prefix(sizes,capacity):
    """Return (accepted_sizes, used_bytes) for the longest fitting ordered prefix.

    sizes must be a list of nonnegative integer byte counts; capacity likewise.
    Inspect/validate all input first, then stop at the first item that will not fit.
    Never reorder packets or skip an oversized packet. Never mutate the input list.
    """
    if type(sizes) is not list:
        raise TypeError('sizes must be a list')
    if type(capacity) is not int or capacity<0:
        raise ValueError('capacity must be a nonnegative integer byte count')
    for size in sizes:
        if type(size) is not int or size<0:
            raise ValueError('sizes must contain nonnegative integer byte counts')
    accepted=[]
    used=0
    for size in sizes:
        if used+size>capacity:
            break
        accepted.append(size)
        used=used+size
    return accepted,used


def format_result(sizes,capacity):
    accepted,used=choose_prefix(sizes,capacity)
    return f'{len(accepted)} packets, {used}/{capacity} payload bytes: {accepted}'


if __name__=='__main__':
    print(format_result([12,7,5],20))
    try:
        choose_prefix([12,-1],20)
    except ValueError as error:
        print(f'rejected input: {error}')
