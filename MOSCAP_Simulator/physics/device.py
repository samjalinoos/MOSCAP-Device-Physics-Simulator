from dataclasses import dataclass
import numpy as np
from physics.materials import (thermal_voltage, intrinsic_carrier_concentration_si, bandgap_si, oxide_capacitance,)


@dataclass
class MOSCAPDevice:
    substrate_type: str      
    doping: float            
    T: float                
    tox_cm: float           
    oxide_k: float           
    phi_m: float             
    Qox: float = 0.0         

    chi_si: float = 4.05     # eV

    def __post_init__(self):
        if self.substrate_type not in ["p", "n"]:
            raise ValueError("substrate_type must be 'p' or 'n'")

        if self.doping <= 0:
            raise ValueError("doping must be positive")

        if self.T <= 0:
            raise ValueError("temperature must be positive")

        if self.tox_cm <= 0:
            raise ValueError("oxide thickness must be positive")

    @property
    def Vt(self):
        return thermal_voltage(self.T)

    @property
    def ni(self):
        return intrinsic_carrier_concentration_si(self.T)

    @property
    def Eg(self):
        return bandgap_si(self.T)

    @property
    def Cox(self):
        return oxide_capacitance(self.tox_cm, self.oxide_k)

    @property
    def phi_f(self):
        return self.Vt * np.log(self.doping / self.ni)

    @property
    def phi_s(self):
        if self.substrate_type == "p":
            return self.chi_si + self.Eg / 2 + self.phi_f

        return self.chi_si + self.Eg / 2 - self.phi_f

    @property
    def Vfb(self):
        return self.phi_m - self.phi_s - self.Qox / self.Cox

    @property
    def Na(self):
        if self.substrate_type == "p":
            return self.doping
        return 0.0

    @property
    def Nd(self):
        if self.substrate_type == "n":
            return self.doping
        return 0.0

    @property
    def p0(self):
        if self.substrate_type == "p":
            return self.doping

        return self.ni**2 / self.doping

    @property
    def n0(self):
        if self.substrate_type == "n":
            return self.doping

        return self.ni**2 / self.doping