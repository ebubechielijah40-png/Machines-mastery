"""Inspectable first-order RC models. SI units throughout; no device safety claim.

The Euler methods intentionally permit unstable step sizes for the local numerical
experiment. They are approximations, not circuit oscillations. No third-party deps.
"""

import math


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def time_constant(r_ohm: float, c_farad: float) -> float:
    """Return R*C in seconds, rejecting unrepresentable model parameters."""
    _positive("r_ohm", r_ohm)
    _positive("c_farad", c_farad)
    tau = r_ohm * c_farad
    _positive("R*C", tau)
    return tau


def rc_response(v_final: float, r_ohm: float, c_farad: float,
                t_sec: float, v_initial: float = 0.0) -> float:
    """Exact ideal constant-input response, including initial stored charge."""
    tau = time_constant(r_ohm, c_farad)
    _finite("v_final", v_final)
    _finite("v_initial", v_initial)
    _finite("t_sec", t_sec)
    if t_sec < 0:
        raise ValueError("t_sec must be nonnegative")
    ratio = t_sec / tau
    # expm1 preserves a very small charging increment; 1-exp(-x) loses it.
    charged_fraction = -math.expm1(-ratio)
    retained_fraction = math.exp(-ratio)
    return v_initial * retained_fraction + v_final * charged_fraction


def rc_charge(v_supply: float, r_ohm: float, c_farad: float,
              t_sec: float) -> float:
    """Compatibility wrapper: initially uncharged ideal capacitor."""
    return rc_response(v_supply, r_ohm, c_farad, t_sec)


def time_to_threshold(v_supply: float, r: float, c: float,
                      v_threshold: float) -> float:
    """Time to a strictly interior positive charging threshold, in seconds."""
    tau = time_constant(r, c)
    _positive("v_supply", v_supply)
    _finite("v_threshold", v_threshold)
    if not 0 < v_threshold < v_supply:
        raise ValueError("threshold must be strictly between zero and supply")
    return -tau * math.log1p(-v_threshold / v_supply)


def loaded_parameters(v_supply: float, r_ohm: float, c_farad: float,
                      r_load_ohm: float,
                      c_probe_farad: float = 0.0) -> tuple[float, float, float]:
    """Return (final V, effective R, total C) for a parallel meter/probe.

    The source connects through r_ohm to a node. Capacitor, r_load_ohm and
    c_probe_farad each connect that node to the reference. All are ideal here.
    """
    time_constant(r_ohm, c_farad)
    _finite("v_supply", v_supply)
    _positive("r_load_ohm", r_load_ohm)
    _finite("c_probe_farad", c_probe_farad)
    if c_probe_farad < 0:
        raise ValueError("c_probe_farad must be nonnegative")
    divider = 1.0 / (1.0 + r_ohm / r_load_ohm)
    r_effective = r_ohm * divider
    c_total = c_farad + c_probe_farad
    time_constant(r_effective, c_total)
    return v_supply * divider, r_effective, c_total


def simulate(v_supply: float, r_ohm: float, c_farad: float,
             dt_sec: float, steps: int, v_initial: float = 0.0,
             method: str = "euler") -> list[tuple[float, float]]:
    """Return (seconds, volts) at steps+1 points, starting with initial state.

    `exact` assumes a constant source over the entire interval. `euler` and
    `backward-euler` expose first-order numerical approximations. Work and
    output memory are O(steps); caller controls experiment size.
    """
    tau = time_constant(r_ohm, c_farad)
    _finite("v_supply", v_supply)
    _finite("v_initial", v_initial)
    _positive("dt_sec", dt_sec)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    if method not in {"euler", "backward-euler", "exact"}:
        raise ValueError("unknown integration method")
    if not math.isfinite(dt_sec * steps):
        raise ValueError("simulation horizon must be finite")
    alpha = dt_sec / tau
    if method != "exact" and not math.isfinite(alpha):
        raise ValueError("dt/tau must be representable")
    result = [(0.0, v_initial)]
    voltage = v_initial
    for index in range(1, steps + 1):
        t_sec = index * dt_sec
        if method == "exact":
            voltage = rc_response(v_supply, r_ohm, c_farad, t_sec, v_initial)
        elif method == "euler":
            voltage += alpha * (v_supply - voltage)
        else:
            # Weighted form avoids alpha*v_supply intermediate overflow.
            retained = 1.0 / (1.0 + alpha)
            voltage = retained * voltage + (1.0 - retained) * v_supply
        if not math.isfinite(voltage):
            raise ValueError("numerical trajectory overflowed; reduce step or horizon")
        result.append((t_sec, voltage))
    return result
