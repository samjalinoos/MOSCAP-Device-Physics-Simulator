import numpy as np
from physics.constants  import q, k_B_J, k_B_eV, eps0

def thermal_voltage(T):
    return k_B_J * T / q

def silicon_permittivity(): 
    return 11.7 * eps0

def oxide_permittivity(oxide_k=3.9):
    return oxide_k * eps0

def bandgap_si(T): 
    Eg0 = 1.17      
    alpha = 4.73e-4  
    beta = 636.0     
    return Eg0 - (alpha * T**2) / (T + beta)

def intrinsic_carrier_concentration_si(T): #ni
    ni_300 = 1.0e10
    T0 = 300.0

    Eg_T = bandgap_si(T)
    Eg_300 = bandgap_si(T0)

    return ni_300 * (T / T0) ** 1.5 * np.exp(
        -Eg_T / (2 * k_B_eV * T)
        + Eg_300 / (2 * k_B_eV * T0)
    )

def oxide_capacitance(tox_cm, oxide_k=3.9):
    eps_ox = oxide_permittivity(oxide_k)
    return eps_ox / tox_cm