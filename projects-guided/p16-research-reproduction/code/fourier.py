"""Original positive-sign radix-2 FFT reconstruction and direct-sum oracle.

The source paper uses exp(+2*pi*i/N). Many APIs call the negative sign 'forward';
do not compare them without reconciling sign/normalization. No NumPy dependency.
"""
import cmath
import math

MAX_POINTS = 4096


def _input(values):
    data=[]
    for value in values:
        if len(data)>=MAX_POINTS:
            raise ValueError('teaching transform limited to 4096 points')
        try: z=complex(value)
        except (ValueError,TypeError,OverflowError) as exc:raise ValueError('finite numeric inputs required') from exc
        if not math.isfinite(z.real) or not math.isfinite(z.imag):raise ValueError('finite numeric inputs required')
        data.append(z)
    if not data:raise ValueError('at least one input required')
    return data


def direct_dft(values):
    """Definition-driven O(N²) oracle; positive sign, no normalization."""
    data=_input(values);n=len(data);result=[]
    for frequency in range(n):
        terms=[value*cmath.exp(2j*math.pi*frequency*index/n) for index,value in enumerate(data)]
        result.append(complex(math.fsum(z.real for z in terms),math.fsum(z.imag for z in terms)))
    return result


def fft_counted(values):
    """Iterative butterflies with an explicit initial bit-reversal permutation.

    Returns (transformed copy, counts). Counts cover loop butterflies/value
    multiplications only, not complex-root generation or interpreter overhead.
    """
    data=_input(values);n=len(data)
    if n&(n-1):raise ValueError('radix-2 FFT requires a positive power-of-two length')
    reverse=0
    for index in range(1,n):
        bit=n>>1
        while reverse&bit:
            reverse^=bit;bit>>=1
        reverse^=bit
        if index<reverse:data[index],data[reverse]=data[reverse],data[index]
    butterflies=0;span=2
    while span<=n:
        half=span//2
        # Compute each root directly: accuracy easier to inspect than recurrence drift.
        roots=[cmath.exp(2j*math.pi*j/span) for j in range(half)]
        for start in range(0,n,span):
            for j,root in enumerate(roots):
                left=data[start+j];right=root*data[start+j+half]
                data[start+j]=left+right;data[start+j+half]=left-right
                butterflies+=1
        span*=2
    return data,{'butterflies':butterflies,'value_complex_multiplications':butterflies,
                 'complex_additions':2*butterflies,'stages':n.bit_length()-1}


def fft(values):return fft_counted(values)[0]


def inverse(values):
    data=_input(values)
    return [z.conjugate()/len(data) for z in fft([z.conjugate() for z in data])]


def circular_convolution(a,b):
    a,b=_input(a),_input(b)
    if len(a)!=len(b):raise ValueError('equal periodic lengths required')
    fa,fb=fft(a),fft(b)
    return inverse([x*y for x,y in zip(fa,fb)])
