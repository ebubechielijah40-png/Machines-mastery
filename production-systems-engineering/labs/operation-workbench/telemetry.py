"""Original bounded cumulative histograms and explicit event-window alerts."""
from fractions import Fraction
import math
from operations import evaluate

STATUSES=('ok','duplicate','overload','deadline','unknown','conflict',
          'storage_unavailable','injected_failure','operation_rejected','internal_error')


def aggregate(records,deadline_ns,bounds_ns=(1_000_000,5_000_000,30_000_000,100_000_000)):
    bounds=tuple(bounds_ns)
    if not 1<=len(bounds)<=16 or any(type(x) is not int or x<=0 for x in bounds) or tuple(sorted(set(bounds)))!=bounds:
        raise ValueError('1..16 increasing positive integer bounds required')
    finite=[]
    for record in records:
        if len(finite)>=5000:raise ValueError('finite observation window exhausted')
        finite.append(record)
    evidence=evaluate(finite,deadline_ns)
    if any(r.status not in STATUSES for r in finite):raise ValueError('unknown metric status')
    result=dict(deadline_ns=deadline_ns,count=len(finite),good=evidence['good'],
                latency_sum_ns=sum(r.latency_ns for r in finite),bounds_ns=list(bounds),
                le_counts=[sum(r.latency_ns<=bound for r in finite) for bound in bounds],
                overflow=sum(r.latency_ns>bounds[-1] for r in finite),
                statuses={s:sum(r.status==s for r in finite) for s in STATUSES})
    validate(result)
    return result


def validate(summary):
    """Structural conservation, not proof that supplied counts came from events."""
    keys={'deadline_ns','count','good','latency_sum_ns','bounds_ns','le_counts','overflow','statuses'}
    if type(summary) is not dict or set(summary)!=keys:raise ValueError('exact summary required')
    if any(type(summary[k]) is not int or not 0<=summary[k]<=10**30 for k in ('deadline_ns','count','good','latency_sum_ns','overflow')):
        raise ValueError('bounded nonnegative counters required')
    if summary['deadline_ns']<1 or summary['good']>summary['count']:raise ValueError('invalid good/deadline counts')
    bounds,counts=summary['bounds_ns'],summary['le_counts']
    if (type(bounds) is not list or not 1<=len(bounds)<=16 or any(type(x) is not int or x<=0 for x in bounds) or
        sorted(set(bounds))!=bounds or type(counts) is not list or len(counts)!=len(bounds) or
        any(type(x) is not int or not 0<=x<=summary['count'] for x in counts) or sorted(counts)!=counts or
        counts[-1]+summary['overflow']!=summary['count']):raise ValueError('invalid cumulative histogram')
    statuses=summary['statuses']
    if type(statuses) is not dict or set(statuses)!=set(STATUSES) or any(type(x) is not int or x<0 for x in statuses.values()) or sum(statuses.values())!=summary['count']:
        raise ValueError('status conservation failed')
    if summary['good']>statuses['ok']+statuses['duplicate']:
        raise ValueError('good events cannot exceed successful/duplicate responses')
    if not summary['count'] and summary['latency_sum_ns']:
        raise ValueError('empty population must have zero latency sum')


def merge(summaries):
    result=None
    for index,summary in enumerate(summaries):
        if index>=128:raise ValueError('at most128 disjoint shards')
        validate(summary)
        if result is None:
            result={**summary,'bounds_ns':summary['bounds_ns'][:],'le_counts':summary['le_counts'][:],'statuses':summary['statuses'].copy()}
        else:
            if (summary['deadline_ns'],summary['bounds_ns'])!=(result['deadline_ns'],result['bounds_ns']):raise ValueError('incompatible configurations')
            for k in ('count','good','latency_sum_ns','overflow'):result[k]+=summary[k]
            result['le_counts']=[a+b for a,b in zip(result['le_counts'],summary['le_counts'])]
            for status in STATUSES:result['statuses'][status]+=summary['statuses'][status]
    if result is None:raise ValueError('explicit configured empty summary required')
    validate(result);return result


def quantile_upper_bound(summary,q):
    validate(summary)
    if type(q) is not Fraction or not 0<q<=1:raise ValueError('exact Fraction quantile required')
    rank=math.ceil(q*summary['count'])
    if not rank:return None
    return next((b for b,c in zip(summary['bounds_ns'],summary['le_counts']) if c>=rank),None)


def burn_alert(short,long,*,target=Fraction(95,100),threshold=Fraction(2),min_short=10,min_long=30):
    """Caller owns normally nested event windows; never add their denominators."""
    validate(short);validate(long)
    if short['deadline_ns']!=long['deadline_ns']:raise ValueError('deadline mismatch')
    if type(target) is not Fraction or not 0<target<1 or type(threshold) is not Fraction or threshold<=0:
        raise ValueError('exact valid policy required')
    if any(type(n) is not int or n<1 for n in (min_short,min_long)):raise ValueError('positive populations required')
    sufficient=short['count']>=min_short and long['count']>=min_long
    rates=[None if not s['count'] else Fraction(s['count']-s['good'],s['count'])/(1-target) for s in (short,long)]
    return dict(status='evaluated' if sufficient else 'insufficient_population',
                short_burn_exact=None if rates[0] is None else str(rates[0]),
                long_burn_exact=None if rates[1] is None else str(rates[1]),
                alert=sufficient and all(r>=threshold for r in rates))
