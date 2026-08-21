import numpy as np
from scipy.optimize import root

from physics.poisson import poisson_residual


def initial_guess(x, Vg, device):
    psi_surface_guess = Vg - device.Vfb

    psi_surface_guess = np.clip(psi_surface_guess, -1.0, 1.0)

    L = x[-1]

    return psi_surface_guess * np.exp(-x / (0.1 * L))


def solve_moscap(Vg, device, x, dx, psi_guess=None):
    if psi_guess is None:
        psi_guess = initial_guess(x, Vg, device)

    result = root(
        fun=poisson_residual,
        x0=psi_guess,
        args=(device, Vg, dx),
        method="lm",
        options={
            "maxiter": 10000,
            "ftol": 1e-12,
            "xtol": 1e-12,
     },
    )

    if not result.success:
        print("Solver warning:", result.message)

    return result.x, result