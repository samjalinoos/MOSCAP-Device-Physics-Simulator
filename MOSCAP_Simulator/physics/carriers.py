import numpy as np

def carrier_densities(psi, device):
    arg = psi / device.Vt
    arg = np.clip(arg, -100, 100)

    n = device.n0 * np.exp(arg)
    p = device.p0 * np.exp(-arg)

    return n, p

def electron_density(psi, device):
    n, _ = carrier_densities(psi, device)
    return n

def hole_density(psi, device):
    _, p = carrier_densities(psi, device)
    return p