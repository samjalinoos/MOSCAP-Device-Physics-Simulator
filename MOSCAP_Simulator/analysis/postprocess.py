import numpy as np

from physics.carriers import carrier_densities
from physics.charge import charge_density
from physics.materials import oxide_permittivity


def electric_field(psi, dx):
    return -np.gradient(psi, dx)


def total_semiconductor_charge(x, psi, device):
    rho = charge_density(psi, device)
    return np.trapezoid(rho, x)


def gate_charge_from_semiconductor(x, psi, device):
    Qs = total_semiconductor_charge(x, psi, device)
    return -Qs - device.Qox


def gate_charge_from_voltage(Vg, psi, device):
    psi_s = psi[0]
    Vox = Vg - device.Vfb - psi_s
    return device.Cox * Vox


def oxide_electric_field_from_voltage(Vg, psi, device):
    psi_s = psi[0]
    Vox = Vg - device.Vfb - psi_s
    return Vox / device.tox_cm


def oxide_electric_field_from_semiconductor_charge(x, psi, device):
    eps_ox = oxide_permittivity(device.oxide_k)
    Qg = gate_charge_from_semiconductor(x, psi, device)
    return Qg / eps_ox


def band_edges(psi, device):
    Ei_bulk = 0.0
    Ec_bulk = device.Eg / 2
    Ev_bulk = -device.Eg / 2

    Ei = Ei_bulk - psi
    Ec = Ec_bulk - psi
    Ev = Ev_bulk - psi

    return Ec, Ei, Ev


def operating_regime(device, psi_s):
    tol = 1e-6

    if abs(psi_s) < tol:
        return "Flat Band"

    if device.substrate_type == "p":
        if psi_s < 0:
            return "Accumulation"
        elif psi_s < 2 * device.phi_f:
            return "Depletion"
        else:
            return "Strong Inversion"

    if device.substrate_type == "n":
        if psi_s > 0:
            return "Accumulation"
        elif psi_s > -2 * device.phi_f:
            return "Depletion"
        else:
            return "Strong Inversion"

    return "Unknown"


def postprocess_solution(x, dx, psi, device, Vg):
    E_si = electric_field(psi, dx)

    n, p = carrier_densities(psi, device)
    rho = charge_density(psi, device)

    Qs = total_semiconductor_charge(x, psi, device)

    Qg_from_semiconductor = gate_charge_from_semiconductor(x, psi, device)
    Qg_from_voltage = gate_charge_from_voltage(Vg, psi, device)

    Eox_from_voltage = oxide_electric_field_from_voltage(Vg, psi, device)
    Eox_from_semiconductor = oxide_electric_field_from_semiconductor_charge(
        x, psi, device
    )

    Ec, Ei, Ev = band_edges(psi, device)

    psi_s = psi[0]
    Vox = Vg - device.Vfb - psi_s
    regime = operating_regime(device, psi_s)

    return {
        "x": x,
        "psi": psi,
        "psi_s": psi_s,
        "regime": regime,

        "E_si": E_si,
        "n": n,
        "p": p,
        "rho": rho,

        "n_surface": n[0],
        "p_surface": p[0],

        "Qs": Qs,

        "Qg": Qg_from_voltage,
        "Qg_from_voltage": Qg_from_voltage,
        "Qg_from_semiconductor": Qg_from_semiconductor,
        "Qg_difference": Qg_from_voltage - Qg_from_semiconductor,

        "Vox": Vox,
        "Eox_voltage": Eox_from_voltage,
        "Eox_charge": Eox_from_semiconductor,
        "Eox_difference": Eox_from_voltage - Eox_from_semiconductor,

        "Ec": Ec,
        "Ei": Ei,
        "Ev": Ev,
    }