#tests if solution is physically sane

import numpy as np

from physics.charge import charge_density
from physics.carriers import carrier_densities
from analysis.postprocess import (
    oxide_electric_field_from_voltage,
    oxide_electric_field_from_semiconductor_charge,
)


def validate_solution(x, dx, psi, device, Vg):
    rho = charge_density(psi, device)
    n, p = carrier_densities(psi, device)

    Eox_voltage = oxide_electric_field_from_voltage(Vg, psi, device)
    Eox_charge = oxide_electric_field_from_semiconductor_charge(x, psi, device)

    eox_abs_diff = abs(Eox_voltage - Eox_charge)

    if abs(Eox_voltage) > 0:
        eox_rel_diff = eox_abs_diff / abs(Eox_voltage)
    else:
        eox_rel_diff = np.nan

    checks = {
        "bulk_potential_error": abs(psi[-1]),
        "rho_bulk": rho[-1],
        "mass_action_max_error": np.max(np.abs(n * p - device.ni**2)),
        "charge_voltage_Eox_difference": eox_abs_diff,
        "relative_Eox_difference": eox_rel_diff,
    }

    return checks