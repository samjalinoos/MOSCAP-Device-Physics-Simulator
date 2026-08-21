# 1D MOSCAP Device Physics Simulator

This is a Python simulator for the electrostatics of a 1D MOS capacitor. It numerically solves the Poisson-Boltzmann equation and plots how potential, charge, carrier concentrations, electric field, and energy bands change with gate bias.

The simulator has an interactive Streamlit interface for changing device parameters and viewing the results. I built this as a practical application of semiconductor device physics and numerical modeling.

<p align="center">
  <img src="screenshots/Interface.png" width="850" alt="MOSCAP simulator interface">
</p>

## Features

* Nonlinear Poisson-Boltzmann solver
* Finite-difference discretization
* p-type and n-type silicon substrates
* Adjustable doping, temperature, oxide thickness, dielectric constant, and gate bias
* Flat-band, accumulation, depletion, and strong inversion regimes
* Carrier concentration, charge density, and electric field profiles
* Energy band diagrams
* Parameter sweeps and validation tools
* Interactive Streamlit interface

## Physical Model

The simulator solves Poisson's equation in the semiconductor:

$$
\frac{d^2\psi}{dx^2} = -\frac{\rho}{\epsilon_{si}}
$$

where $\psi$ is the electrostatic potential and $\rho$ is the local charge density.

The semiconductor charge density is

$$
\rho = q(p-n+N_D-N_A)
$$

with electron and hole concentrations calculated using Boltzmann statistics:

$$
n = n_0 e^{\psi/V_T}
$$

$$
p = p_0 e^{-\psi/V_T}
$$

Because the carrier concentrations depend on the electrostatic potential while the potential depends on the resulting charge density, the equations form a nonlinear system that must be solved numerically.

## Numerical Method

The semiconductor is represented by a uniform 1D grid. Poisson's equation is discretized using a central finite-difference approximation:

$$
\frac{d^2\psi}{dx^2}
\approx
\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{\Delta x^2}
$$

This converts the differential equation and boundary conditions into a system of coupled nonlinear equations for the potential at each grid point.

The system is solved using `scipy.optimize.root`. Once the potential profile has converged, the simulator calculates the carrier concentrations, charge density, electric field, surface potential, and energy-band profiles.

For gate-voltage sweeps, the converged solution from one bias point is used as the initial guess for the next.

## Operating Regimes

The simulator reproduces the standard electrostatic regimes of a MOS capacitor:

**Flat band** — At $V_g-V_{fb}=0$, the surface potential is approximately zero and the semiconductor bands remain nearly flat.

**Accumulation** — For a p-type substrate, negative gate bias attracts holes toward the oxide-semiconductor interface.

**Depletion** — Moderate positive bias repels holes from the surface, leaving behind ionized acceptor atoms and forming a depletion region.

**Strong inversion** — At sufficiently positive gate bias, electrons become the dominant carrier near the surface and form an inversion layer.

The same model can also simulate n-type substrates with the corresponding carrier behavior reversed.

## Example Results

### Carrier Densities

<p align="center">
  <img src="screenshots/carrierdensities.png" width="750" alt="MOSCAP carrier density profiles">
</p>

### Strong Inversion

<p align="center">
  <img src="screenshots/stronginversion.png" width="750" alt="MOSCAP strong inversion">
</p>

## Outputs

For a selected device and bias condition, the simulator calculates and displays:

* Electrostatic potential $\psi(x)$
* Electric field $E(x)$
* Electron concentration $n(x)$
* Hole concentration $p(x)$
* Space-charge density $\rho(x)$
* Surface potential $\psi_s$
* Surface carrier concentrations
* MOSCAP operating regime
* Conduction, intrinsic, and valence band profiles

## Validation

The simulator includes several checks for numerical and physical consistency.

The potential and charge density are checked at the bulk boundary, and the calculated carrier concentrations are tested against the mass-action relation

$$
np=n_i^2
$$

The oxide electric field is also calculated independently from the oxide voltage drop and from the integrated semiconductor charge. Agreement between the two provides an additional check on the electrostatic solution.

The model reproduces the expected progression from accumulation through depletion to strong inversion as gate bias is varied.

## Running the Simulator

Install the required packages:

```bash
pip install numpy scipy matplotlib streamlit
```

Then run:

```bash
streamlit run app.py
```

## Project Structure

```text
.
├── app.py
├── styles.py
├── physics/
│   ├── constants.py
│   ├── materials.py
│   ├── device.py
│   ├── grid.py
│   ├── carriers.py
│   ├── charge.py
│   ├── poisson.py
│   └── solver.py
└── analysis/
    ├── postprocess.py
    ├── sweep.py
    ├── validation.py
    └── plots.py
```

## Limitations

This is a simplified electrostatic model rather than a full TCAD device simulator, so it assumes one dimensional electrostatics, classical Boltzmann carrier statistics, and equilibrium carrier distributions.
