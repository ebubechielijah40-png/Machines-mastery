"""Original small dense linear mechanisms; scalar loops, no array library.

Matrix convention is output rows, input columns. Dot is a Hermitian inner
product, whereas matrix multiplication does not conjugate either factor.
All inputs are locally controlled; this is not a resource-isolated service.
"""
import math


def finite(x):
    if isinstance(x, bool) or not isinstance(x, (int, float, complex)):
        raise ValueError('expected a real or complex number, not bool')
    try:
        z = complex(x)
    except OverflowError as exc:
        raise ValueError('unrepresentable numeric magnitude') from exc
    if not math.isfinite(z.real) or not math.isfinite(z.imag):
        raise ValueError('nonfinite arithmetic')
    return x


def vector(xs):
    data = [finite(x) for x in xs]
    if not data:
        raise ValueError('empty vectors are outside this model')
    return data


def matrix(rows):
    data = [vector(row) for row in rows]
    if not data or any(len(row) != len(data[0]) for row in data):
        raise ValueError('matrix must be nonempty and rectangular')
    return data


def dot(a, b):
    a, b = vector(a), vector(b)
    if len(a) != len(b):
        raise ValueError('dot-product dimensions disagree')
    return finite(sum(x.conjugate()*y for x, y in zip(a, b)))


def matvec(a, x):
    a, x = matrix(a), vector(x)
    if len(a[0]) != len(x):
        raise ValueError('matrix columns must equal vector length')
    return [finite(sum(v*w for v, w in zip(row, x))) for row in a]


def transpose(a, conjugate=False):
    a = matrix(a)
    return [[a[i][j].conjugate() if conjugate else a[i][j]
             for i in range(len(a))] for j in range(len(a[0]))]


def matmul(a, b):
    a, b = matrix(a), matrix(b)
    if len(a[0]) != len(b):
        raise ValueError('inner matrix dimensions disagree')
    return [[finite(sum(a[i][k]*b[k][j] for k in range(len(b))))
             for j in range(len(b[0]))] for i in range(len(a))]


def identity(n):
    if type(n) is not int or not 1 <= n <= 256:
        raise ValueError('identity size must be an integer from1 to256')
    return [[int(i == j) for j in range(n)] for i in range(n)]


def solve(a, b, rtol=1e-12):
    """Real square system via row scaling, partial pivoting and back substitution.

    Pivot rejection means numerically unresolved at this tolerance, not proof
    of exact singularity. Finite float range/rounding still apply. O(n³) time,
    O(n²) memory; n<=64 is a teaching guard.
    """
    a, b = matrix(a), vector(b)
    n = len(a)
    if n > 64 or len(a[0]) != n or len(b) != n:
        raise ValueError('need square A and compatible b, with1<=n<=64')
    if any(isinstance(x, complex) for row in a for x in row) or any(isinstance(x, complex) for x in b):
        raise ValueError('this solver accepts real systems only')
    finite(rtol)
    if isinstance(rtol,complex) or not 0 <= rtol < 1:
        raise ValueError('rtol must be in [0,1)')
    work=[]
    for row, rhs in zip(a, b):
        scale=max(abs(x) for x in row)
        if scale == 0:
            raise ValueError('zero row: no unique solution')
        work.append([finite(float(x/scale)) for x in row]+[finite(float(rhs/scale))])
    for col in range(n):
        pivot=max(range(col,n),key=lambda i:abs(work[i][col]))
        if abs(work[pivot][col]) <= rtol:
            raise ValueError('singular or numerically unresolved pivot')
        work[col],work[pivot]=work[pivot],work[col]
        for i in range(col+1,n):
            factor=work[i][col]/work[col][col]
            work[i][col]=0.0
            for j in range(col+1,n+1):
                work[i][j]=finite(work[i][j]-factor*work[col][j])
    x=[0.0]*n
    for i in reversed(range(n)):
        remaining=math.fsum(work[i][j]*x[j] for j in range(i+1,n))
        x[i]=finite((work[i][n]-remaining)/work[i][i])
    return x


def quadratic_loss_gradient(a, b, x):
    """Return 1/2||Ax-b||² and Aᵀ(Ax-b), for finite real inputs."""
    a, b, x = matrix(a), vector(b), vector(x)
    if any(isinstance(v, complex) for row in a for v in row) or any(isinstance(v, complex) for v in b+x):
        raise ValueError('this real loss excludes complex differentiation')
    prediction=matvec(a,x)
    if len(b) != len(prediction):
        raise ValueError('target dimension disagrees')
    residual=[finite(p-y) for p,y in zip(prediction,b)]
    loss=finite(0.5*math.fsum(v*v for v in residual))
    gradient=matvec(transpose(a),residual)
    return loss,gradient


def gradient_steps(a,b,x,learning_rate,steps):
    """Fixed-step descent: deliberately permits unstable steps for experiment."""
    x=vector(x)
    finite(learning_rate)
    if isinstance(learning_rate,complex) or learning_rate<=0 or type(steps) is not int or not 0<=steps<=10000:
        raise ValueError('positive real rate and0<=steps<=10000 required')
    history=[]
    for step in range(steps+1):
        loss,gradient=quadratic_loss_gradient(a,b,x)
        history.append({'step':step,'x':x[:],'loss':loss})
        if step<steps:
            x=[finite(v-learning_rate*g) for v,g in zip(x,gradient)]
    return history
