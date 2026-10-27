"""SI-only, finite teaching models; no certified material parameters or hardware."""
from dataclasses import dataclass
import math


def real(value, name='value', *, positive=False, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name} must be a finite real scalar')
    try:
        value = float(value)
    except (OverflowError, ValueError):
        raise ValueError(f'{name} is not representable') from None
    if not math.isfinite(value) or (positive and value <= 0) or (nonnegative and value < 0):
        raise ValueError(f'{name} is outside its finite range')
    return value


def calculated(value):
    return real(value, 'calculated output')


def numbers(values, name, minimum=1):
    try:
        iterator = iter(values)
    except TypeError:
        raise ValueError(f'{name} must be a finite iterable') from None
    items = []
    for index, value in enumerate(iterator):
        if index == 10000:
            raise ValueError('at most 10000 elements are supported')
        items.append(real(value, name))
    if len(items) < minimum:
        raise ValueError(f'need at least {minimum} elements')
    return items


@dataclass(frozen=True)
class BondLaw:
    """U=D/(m-1)[(r0/r)^m-m*r0/r], for 0.25 <= r/r0 <= 10."""
    depth_J: float
    spacing_m: float
    exponent: int = 8

    def __post_init__(self):
        for field in ('depth_J', 'spacing_m'):
            object.__setattr__(self, field, real(getattr(self, field), field, positive=True))
        if type(self.exponent) is not int or not 2 <= self.exponent <= 20:
            raise ValueError('exponent must be an integer in [2,20]')
        real(self.stiffness_N_per_m, 'stiffness', positive=True)

    @property
    def stiffness_N_per_m(self):
        return calculated(self.depth_J / self.spacing_m / self.spacing_m * self.exponent)

    def _q(self, r):
        r = real(r, 'separation_m', positive=True)
        ratio = r / self.spacing_m
        if not .25 <= ratio <= 10:
            raise ValueError('separation outside declared numerical envelope')
        return 1 / ratio

    def energy_J(self, r):
        q = self._q(r); m = self.exponent
        return calculated(self.depth_J / (m - 1) * (q**m - m*q))

    def required_force_N(self, r):
        q = self._q(r); m = self.exponent
        # expm1 retains the zero at q=1 without subtracting nearly equal powers.
        difference = -q*q * math.expm1((m - 1)*math.log(q))
        return calculated(self.depth_J / self.spacing_m * m / (m - 1) * difference)

    def tangent_N_per_m(self, r):
        q = self._q(r); m = self.exponent
        return calculated(self.depth_J / self.spacing_m / self.spacing_m * m / (m - 1)
                          * ((m + 1)*q**(m + 2) - 2*q**3))

    def force_peak_separation_m(self):
        return calculated(self.spacing_m * ((self.exponent + 1)/2)**(1/(self.exponent - 1)))

    def ideal_chain_modulus_Pa(self):
        """Only the explicitly defined parallel-chain geometry, not a real crystal."""
        return real(self.stiffness_N_per_m / self.spacing_m, 'ideal-chain modulus', positive=True)


@dataclass(frozen=True)
class Bar:
    length_m: float
    area_m2: float
    modulus_Pa: float
    max_abs_strain: float = .01

    def __post_init__(self):
        for field in ('length_m', 'area_m2', 'modulus_Pa', 'max_abs_strain'):
            object.__setattr__(self, field, real(getattr(self, field), field, positive=True))
        real(self.compliance_m_per_N, 'compliance', positive=True)

    @property
    def compliance_m_per_N(self):
        return calculated(self.length_m / self.area_m2 / self.modulus_Pa)

    def response(self, force_N):
        f = real(force_N, 'force_N')
        stress = calculated(f / self.area_m2)
        strain = calculated(stress / self.modulus_Pa)
        if abs(strain) > self.max_abs_strain:
            raise ValueError('outside declared linear strain envelope')
        extension = calculated(strain * self.length_m)
        return {'stress_Pa': stress, 'strain': strain, 'extension_m': extension,
                'stored_energy_J': calculated(.5*f*extension)}


def series_compliance(compliances):
    items = numbers(compliances, 'compliance')
    if any(c <= 0 for c in items):
        raise ValueError('compliances must be positive')
    try:
        return calculated(math.fsum(items))
    except OverflowError:
        raise ValueError('series arithmetic outside finite envelope') from None


def parallel_compliance(compliances):
    items = numbers(compliances, 'compliance')
    if any(c <= 0 for c in items):
        raise ValueError('compliances must be positive')
    # Normalize by smallest compliance to avoid reciprocal overflow.
    minimum = min(items)
    return real(minimum / math.fsum(minimum/c for c in items), 'parallel compliance', positive=True)


@dataclass(frozen=True)
class Fit:
    slope_m_per_N: float
    intercept_m: float
    slope_standard_uncertainty_m_per_N: float
    residuals_m: tuple


def fit_extension(forces_N, extensions_m):
    """OLS with an intercept. Uncertainty formula assumes fixed true loads/iid noise."""
    x = numbers(forces_N, 'force_N', 3)
    y = numbers(extensions_m, 'extension_m', 3)
    n = len(x)
    if n != len(y) or not 3 <= n <= 10000:
        raise ValueError('need equally sized arrays of 3..10000 observations')
    try:
        mean_x, mean_y = math.fsum(x)/n, math.fsum(y)/n
        dx = [v - mean_x for v in x]
        sxx = real(math.fsum(v*v for v in dx), 'load spread', positive=True)
        sxy = real(math.fsum(a*(b - mean_y) for a, b in zip(dx, y)), 'cross sum')
        slope = calculated(sxy/sxx)
        intercept = calculated(mean_y - slope*mean_x)
        residuals = tuple(calculated(b - (intercept + slope*a)) for a, b in zip(x, y))
        residual_variance = calculated(math.fsum(v*v for v in residuals)/(n - 2))
        uncertainty = calculated(math.sqrt(residual_variance/sxx))
    except (OverflowError, ZeroDivisionError):
        raise ValueError('fit arithmetic outside finite envelope') from None
    return Fit(slope, intercept, uncertainty, residuals)


def infer_modulus(length_m, area_m2, measured_slope, frame_compliance=0):
    length = real(length_m, 'length_m', positive=True)
    area = real(area_m2, 'area_m2', positive=True)
    slope = real(measured_slope, 'measured_slope', positive=True)
    frame = real(frame_compliance, 'frame_compliance', nonnegative=True)
    specimen = real(slope - frame, 'specimen compliance', positive=True)
    return real(length / area / specimen, 'modulus_Pa', positive=True)


def infer_two_lengths(length1, slope1, length2, slope2, area_m2):
    l1, l2 = (real(v, 'length', positive=True) for v in (length1, length2))
    s1, s2 = (real(v, 'slope', positive=True) for v in (slope1, slope2))
    area = real(area_m2, 'area_m2', positive=True)
    if l2 <= l1 or s2 <= s1:
        raise ValueError('ordered distinct lengths and increasing slopes required')
    modulus = real((l2 - l1)/area/(s2 - s1), 'modulus_Pa', positive=True)
    frame = calculated(s1 - l1/area/modulus)
    # Small negative fit estimates remain diagnostic evidence, not silently clipped.
    return {'modulus_Pa': modulus, 'frame_compliance_m_per_N': frame}


def relative_standard_uncertainty(length, u_length, area, u_area, slope, u_slope):
    values = [(real(v, 'quantity', positive=True), real(u, 'standard uncertainty', nonnegative=True))
              for v, u in ((length, u_length), (area, u_area), (slope, u_slope))]
    return calculated(math.hypot(*(u/v for v, u in values)))
