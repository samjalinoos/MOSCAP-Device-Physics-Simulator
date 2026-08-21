import numpy as np

from physics.materials import silicon_permittivity, oxide_permittivity
from physics.charge import charge_density


def poisson_residual(psi, device, Vg, dx):
    eps_si = silicon_permittivity()
    eps_ox = oxide_permittivity(device.oxide_k)

    R = np.zeros_like(psi)

    Esi_surface = -(psi[1] - psi[0]) / dx
    Vox = device.tox_cm * (eps_si / eps_ox) * Esi_surface

    R[0] = Vg - device.Vfb - psi[0] - Vox

    rho = charge_density(psi, device)

    for i in range(1, len(psi) - 1):
        R[i] = (
            psi[i + 1]
            - 2 * psi[i]
            + psi[i - 1]
            + dx**2 * rho[i] / eps_si
        )

    R[-1] = psi[-1]

    return R