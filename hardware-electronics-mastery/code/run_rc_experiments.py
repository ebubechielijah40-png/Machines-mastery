"""Small deterministic numerical investigations; writes JSON only to stdout.

Run from repository root:
    python3 hardware-electronics-mastery/code/run_rc_experiments.py > /tmp/rc.json
The output consists of simulated data, never physical measurements.
"""
import json
import math
import platform
import sys

from rc_lab import (loaded_parameters, rc_charge, rc_response, simulate,
                    time_constant, time_to_threshold)


def investigate():
    supply, r, c = 3.3, 10_000.0, 10e-6
    tau = time_constant(r, c)
    exact_at_tau = rc_charge(supply, r, c, tau)
    convergence = []
    for steps in (10, 20, 40, 80, 160):
        row = {"steps": steps, "dt_s": tau / steps}
        for method in ("euler", "backward-euler", "exact"):
            voltage = simulate(supply, r, c, tau / steps, steps,
                               method=method)[-1][1]
            row[method] = {"voltage_V": voltage,
                           "absolute_error_V": abs(voltage - exact_at_tau)}
        convergence.append(row)
    stability = []
    for alpha in (0.5, 1.5, 2.0, 2.5):
        stability.append({"dt_over_tau": alpha,
                          "error_multiplier": 1 - alpha,
                          "trajectory": [{"t_s": t, "voltage_V": v}
                                         for t, v in simulate(supply, r, c,
                                                              alpha*tau, 10)]})
    loaded_final, effective_r, total_c = loaded_parameters(
        supply, 100_000, 1e-6, 1_000_000, 100e-12)
    loaded_tau = time_constant(effective_r, total_c)
    sample_time = 0.05
    loaded_voltage = rc_response(loaded_final, effective_r, total_c, sample_time)
    # Same generated sample, two assumed final voltages: model bias is visible.
    wrong_tau = -sample_time / math.log1p(-loaded_voltage / supply)
    corrected_tau = -sample_time / math.log1p(-loaded_voltage / loaded_final)
    nominal_tau = 100_000 * 1e-6
    relative_u = math.sqrt((0.01**2 + 0.10**2) / 3)
    return {
        "data_kind": "deterministic ideal-model simulation; no physical circuit measured",
        "environment": {"python": sys.version, "platform": platform.platform()},
        "base_parameters": {"supply_V": supply, "resistance_ohm": r,
                            "capacitance_F": c, "initial_voltage_V": 0,
                            "tau_s": tau},
        "analytic_checks": {"voltage_at_tau_V": exact_at_tau,
                            "half_supply_time_s": time_to_threshold(supply, r, c,
                                                                    supply / 2),
                            "source_energy_infinite_time_J": c*supply*supply,
                            "capacitor_energy_infinite_time_J": 0.5*c*supply*supply},
        "convergence_fixed_time_tau": convergence,
        "stability": stability,
        "instrument_loading": {
            "source_resistance_ohm": 100_000, "capacitance_F": 1e-6,
            "meter_resistance_ohm": 1_000_000, "probe_capacitance_F": 100e-12,
            "unloaded_tau_s": nominal_tau, "loaded_final_V": loaded_final,
            "loaded_tau_s": loaded_tau, "sample_time_s": sample_time,
            "synthetic_voltage_V": loaded_voltage,
            "tau_inferred_assuming_3_3V_final_s": wrong_tau,
            "tau_inferred_using_3_0V_final_s": corrected_tau},
        "component_tolerance_model": {
            "kind": "hypothetical independent uniform component errors; not measured",
            "resistance_relative_bound": 0.01, "capacitance_relative_bound": 0.10,
            "tau_worst_case_interval_s": [tau*0.99*0.9, tau*1.01*1.1],
            "tau_linearized_standard_uncertainty_s": tau*relative_u},
    }


if __name__ == "__main__":
    print(json.dumps(investigate(), indent=2, allow_nan=False))
