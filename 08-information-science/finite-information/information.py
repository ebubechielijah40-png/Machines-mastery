"""Original finite-distribution entropy calculation, not an entropy estimator proof."""
import math
import itertools


def distribution(weights):
    values=list(itertools.islice(weights,4097))
    if not 1<=len(values)<=4096:raise ValueError('one to 4096 weights required')
    try:
        if any(type(x) not in (int,float) or not math.isfinite(x) or x<0 for x in values):
            raise ValueError('finite nonnegative numeric weights required')
        total=math.fsum(values)
    except OverflowError as exc:
        raise ValueError('weights exceed floating calculation range') from exc
    if not math.isfinite(total) or total<=0:raise ValueError('positive finite total required')
    return [x/total for x in values]


def entropy(weights):
    return -math.fsum(p*math.log2(p) for p in distribution(weights) if p>0)


def joint_information(weights):
    rows=[list(itertools.islice(row,65)) for row in itertools.islice(weights,65)]
    if not 1<=len(rows)<=64 or not 1<=len(rows[0])<=64 or any(len(row)!=len(rows[0]) for row in rows):
        raise ValueError('rectangular 1..64 by 1..64 joint table required')
    flat=distribution(x for row in rows for x in row)
    width=len(rows[0]);p=[flat[i:i+width] for i in range(0,len(flat),width)]
    row_mass=[math.fsum(row) for row in p]
    col_mass=[math.fsum(row[j] for row in p) for j in range(width)]
    hx=entropy(row_mass);hy=entropy(col_mass);hxy=entropy(flat)
    return {'h_x':hx,'h_y':hy,'h_joint':hxy,'h_x_given_y':hxy-hy,'h_y_given_x':hxy-hx,'mutual_information':hx+hy-hxy}
