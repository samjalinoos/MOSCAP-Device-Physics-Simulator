from physics.constants import q
from physics.carriers import carrier_densities


def charge_density(psi, device):
    n, p = carrier_densities(psi, device)

    rho = q * (p - n + device.Nd - device.Na)

    return rho