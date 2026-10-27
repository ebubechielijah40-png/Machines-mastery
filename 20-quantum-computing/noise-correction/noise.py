"""Original bounded one-qubit channels and ideal three-qubit repetition recovery.

Index i denotes |q2 q1 q0>; parity syndrome is (q0 XOR q1, q1 XOR q2).
All channels and error probabilities are synthetic; no hardware/library backend.
"""
import math

TOL = 1e-10
I = ((1, 0), (0, 1))
X = ((0, 1), (1, 0))
Z = ((1, 0), (0, -1))
H = ((1/math.sqrt(2), 1/math.sqrt(2)), (1/math.sqrt(2), -1/math.sqrt(2)))


def scalar(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, complex)):
        raise ValueError('finite numeric entries required')
    try:
        z = complex(value)
    except OverflowError as exc:
        raise ValueError('numeric entry exceeds representable complex range') from exc
    if not math.isfinite(z.real) or not math.isfinite(z.imag):
        raise ValueError('finite numeric entries required')
    return z


def probability(p):
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not 0 <= p <= 1:
        raise ValueError('probability must be finite and between zero and one')
    return p


def matrix(values):
    if len(values) != 2 or any(len(row) != 2 for row in values):
        raise ValueError('two-by-two matrix required')
    return tuple(tuple(scalar(v) for v in row) for row in values)


def dagger(a):
    a = matrix(a)
    return tuple(tuple(a[j][i].conjugate() for j in range(2)) for i in range(2))


def mul(a, b):
    a, b = matrix(a), matrix(b)
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def scale(a, t):
    a, t = matrix(a), scalar(t)
    return tuple(tuple(t*x for x in row) for row in a)


def total(matrices):
    return tuple(tuple(sum(a[i][j] for a in matrices) for j in range(2)) for i in range(2))


def density(a):
    """Validate a qubit density matrix; never repair or silently renormalize."""
    a = matrix(a)
    if any(abs(a[i][j]-a[j][i].conjugate()) > TOL for i in range(2) for j in range(2)):
        raise ValueError('density matrix must be Hermitian')
    if abs(a[0][0]+a[1][1]-1) > TOL:
        raise ValueError('density trace must be one')
    determinant = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    if a[0][0].real < -TOL or a[1][1].real < -TOL or determinant.real < -TOL:
        raise ValueError('density matrix must be positive semidefinite')
    return a


def pure(a, b):
    a, b = scalar(a), scalar(b)
    norm = math.hypot(a.real,a.imag,b.real,b.imag)
    if not .5 <= norm <= 2 or abs(norm*norm-1) > TOL:
        raise ValueError('state must be normalized')
    return density(((a*a.conjugate(), a*b.conjugate()), (b*a.conjugate(), b*b.conjugate())))


def channel(rho, kraus):
    rho = density(rho)
    if not 1 <= len(kraus) <= 16:
        raise ValueError('one through sixteen Kraus operators required by this bounded model')
    operators = [matrix(a) for a in kraus]
    completeness = total([mul(dagger(a), a) for a in operators])
    if any(abs(completeness[i][j]-I[i][j]) > TOL for i in range(2) for j in range(2)):
        raise ValueError('Kraus completeness must equal identity')
    return density(total([mul(mul(a, rho), dagger(a)) for a in operators]))


def phase_flip(rho, p):
    p = probability(p)
    return channel(rho, [scale(I, math.sqrt(1-p)), scale(Z, math.sqrt(p))])


def bit_flip(rho, p):
    p = probability(p)
    return channel(rho, [scale(I, math.sqrt(1-p)), scale(X, math.sqrt(p))])


def relax(rho, gamma):
    gamma = probability(gamma)
    return channel(rho, [((1, 0), (0, math.sqrt(1-gamma))), ((0, math.sqrt(gamma)), (0, 0))])


def purity(rho):
    square = mul(density(rho), density(rho))
    return (square[0][0]+square[1][1]).real


def z_probabilities(rho):
    rho = density(rho)
    return tuple(max(0.0, min(1.0, rho[i][i].real)) for i in range(2))


def vector(state):
    if len(state) != 8:
        raise ValueError('three-qubit state must have eight amplitudes')
    values = tuple(scalar(a) for a in state)
    norm = math.hypot(*(component for a in values for component in (a.real,a.imag)))
    if not .5 <= norm <= 2 or abs(norm*norm-1) > TOL:
        raise ValueError('state must be normalized')
    return values


def encode(a, b):
    pure(a, b)
    return vector((a, 0, 0, 0, 0, 0, 0, b))


def flip_mask(state, mask):
    state = vector(state)
    if type(mask) is not int or not 0 <= mask < 8:
        raise ValueError('three-bit error mask required')
    return tuple(state[j ^ mask] for j in range(8))


def phase_error(state, qubit):
    state = vector(state)
    if type(qubit) is not int or not 0 <= qubit < 3:
        raise ValueError('qubit must be zero, one or two')
    return tuple((-a if (j >> qubit) & 1 else a) for j, a in enumerate(state))


def syndrome(index):
    return ((index & 1) ^ ((index >> 1) & 1), ((index >> 1) & 1) ^ ((index >> 2) & 1))


def recover(state):
    """Exact projective parity measurement, then perfect conditional X correction.

    Return separate normalized branches and their probabilities. Do not add
    branch amplitudes: syndrome measurement makes them a classical mixture.
    """
    state = vector(state)
    correction = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 4}
    branches = []
    for outcome, mask in correction.items():
        projected = [a if syndrome(j) == outcome else 0j for j, a in enumerate(state)]
        p = sum(abs(a)**2 for a in projected)
        if p > 0:
            normalized = tuple(a/math.sqrt(p) for a in projected)
            branches.append((outcome, p, flip_mask(normalized, mask)))
    return branches


def logical_density(state):
    state = vector(state)
    if any(abs(state[j]) > TOL for j in range(1, 7)):
        raise ValueError('state is outside repetition-code subspace')
    return pure(state[0], state[7])


def corrected_bit_noise(a, b, p):
    """Average all eight independent error masks and exact recovery branches."""
    p = probability(p)
    state = encode(a, b)
    terms = []
    for mask in range(8):
        weight = mask.bit_count()
        chance = p**weight*(1-p)**(3-weight)
        for _, branch_p, corrected in recover(flip_mask(state, mask)):
            terms.append(scale(logical_density(corrected), chance*branch_p))
    return density(total(terms))


def logical_error_probability(p):
    """Enumerate majority-failing masks, not the closed-form oracle used in tests."""
    p = probability(p)
    return sum(p**mask.bit_count()*(1-p)**(3-mask.bit_count())
               for mask in range(8) if mask.bit_count() >= 2)
