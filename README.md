# 1D MOSCAP Device Physics Simulator

A Python simulator for the electrostatics of a one-dimensional metal-oxide-semiconductor capacitor (MOSCAP). It numerically solves the nonlinear Poisson-Boltzmann equation and calculates how potential, carrier concentrations, charge density, electric field, and energy bands change with gate bias and device parameters.

An interactive Streamlit interface allows device parameters to be changed and the resulting profiles viewed in real time.

## Features

* Nonlinear Poisson-Boltzmann solver
* Finite-difference discretization in one dimension
* p-type and n-type silicon substrates
* Adjustable doping concentration and temperature
* Adjustable oxide thickness and dielectric constant
* Adjustable gate work function and gate bias
* Flat-band, accumulation, depletion, and strong inversion regimes
* Electron and hole concentration profiles
* Space-charge and electric-field profiles
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

where $n$ and $p$ are the electron and hole concentrations, and $N_D$ and $N_A$ are the donor and acceptor concentrations.

Carrier concentrations are calculated using Boltzmann statistics:

$$
n = n_0 e^{\psi/V_T}
$$

$$
p = p_0 e^{-\psi/V_T}
$$

Because the carrier concentrations depend on the electrostatic potential while the potential itself depends on the resulting charge density, the equations form a nonlinear system.

The model assumes that the important electrostatic variation occurs perpendicular to the oxide-semiconductor interface, reducing the device to one dimension.

Deep within the semiconductor, the potential approaches its equilibrium value:

$$
\psi(x \rightarrow \infty) = 0
$$

At the oxide-semiconductor interface, the surface boundary condition accounts for the applied gate voltage, flat-band voltage, oxide thickness, and electric fields in the oxide and semiconductor.

## Numerical Method

The semiconductor is divided into a uniform one-dimensional grid. Poisson's equation is discretized using a central finite-difference approximation:

$$
\frac{d^2\psi}{dx^2}
\approx
\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{\Delta x^2}
$$

Applying this equation at each interior grid point converts the continuous differential equation into a system of coupled nonlinear algebraic equations.

The resulting system is solved using `scipy.optimize.root`. An initial potential profile is supplied to the solver, which iterates until the residual of the discretized equations converges.

Once $\psi(x)$ has been found, the remaining quantities are calculated from the solution:

$$
E(x) = -\frac{d\psi}{dx}
$$

along with the electron and hole concentrations, charge density, surface potential, and energy-band profiles.

For gate-voltage sweeps, the converged solution at one bias point is used as the initial guess for the next bias point.

## MOSCAP Operating Regimes

The simulator reproduces the main electrostatic operating regimes of a MOS capacitor.

### Flat Band

At

$$
V_g - V_{fb} = 0
$$

the surface potential is approximately zero and little band bending occurs. Carrier concentrations remain close to their equilibrium values throughout the semiconductor.

### Accumulation

For a p-type substrate, negative gate bias attracts holes toward the oxide-semiconductor interface. The majority-carrier concentration therefore increases near the surface.

### Depletion

As the gate voltage becomes more positive, holes are repelled from the semiconductor surface. Ionized acceptor atoms remain behind, producing a region of fixed negative space charge.

### Strong Inversion

At sufficiently positive gate bias, the electron concentration near the surface becomes greater than the hole concentration and an inversion layer forms.

The simulator identifies strong inversion using the surface-potential condition

$$
\psi_s > 2\phi_F
$$

for a p-type substrate.

The corresponding behavior is reversed for an n-type substrate.

## Simulation Outputs

For a selected device and bias condition, the simulator calculates:

* Electrostatic potential $\psi(x)$
* Electric field $E(x)$
* Electron concentration $n(x)$
* Hole concentration $p(x)$
* Space-charge density $\rho(x)$
* Surface potential $\psi_s$
* Surface carrier concentrations
* Flat-band voltage $V_{fb}$
* MOSCAP operating regime
* Conduction band $E_C$
* Intrinsic energy level $E_i$
* Valence band $E_V$

The Streamlit interface plots these quantities as a function of depth into the semiconductor.

## Validation

Several checks are included to test whether a converged numerical solution is physically consistent.

### Bulk Boundary

The potential should approach zero deep within the semiconductor:

$$
\psi(x_{\text{bulk}}) \approx 0
$$

and the bulk charge density should approach its equilibrium value.

### Mass-Action Relation

The calculated carrier concentrations are checked against

$$
np = n_i^2
$$

throughout the semiconductor.

### Oxide Field Consistency

The oxide electric field is calculated in two independent ways.

From the voltage drop across the oxide:

$$
E_{ox} = \frac{V_g-V_{fb}-\psi_s}{t_{ox}}
$$

and from the semiconductor charge using Gauss's law.

Agreement between the two provides a consistency check between the solved semiconductor charge distribution and the applied gate voltage.

The simulator also reproduces the expected progression from accumulation through depletion to strong inversion as gate bias is varied.

## Interactive Interface

The Streamlit interface includes several starting configurations:

* P-type baseline
* N-type baseline
* Thin oxide
* Heavy doping
* High-$k$ oxide

The following parameters can be changed directly:

* Semiconductor type
* Doping concentration
* Temperature
* Oxide thickness
* Relative oxide permittivity
* Gate work function
* Effective gate bias
* Simulation depth
* Numerical grid resolution

The interface displays the current operating regime, surface potential, flat-band voltage, inversion threshold, and surface carrier concentrations alongside the solved profiles.

## Running the Simulator

Install the required packages:

```bash
pip install numpy scipy matplotlib streamlit
```

From the project directory, run:

```bash
streamlit run app.py
```

Streamlit will launch the simulator in a browser.

## Project Structure

```text
.
├── app.py
├── styles.py
│
├── physics/
│   ├── constants.py
│   ├── materials.py
│   ├── device.py
│   ├── grid.py
│   ├── carriers.py
│   ├── charge.py
│   ├── poisson.py
│   └── solver.py
│
└── analysis/
    ├── postprocess.py
    ├── sweep.py
    ├── validation.py
    └── plots.py
```

The `physics` modules contain the device model and numerical solver, while `analysis` contains postprocessing, parameter sweeps, validation, and plotting utilities.

## Limitations

This is a simplified electrostatic model rather than a full TCAD device simulator.

The current model assumes:

* One-dimensional electrostatics
* Classical Boltzmann carrier statistics
* Equilibrium carrier distributions
* No carrier transport
* No quantum confinement or tunneling
* No recombination or generation
* No interface traps
* No mobility effects

Boltzmann statistics also become less accurate at sufficiently high doping concentrations, where Fermi-Dirac statistics are required.

The model is therefore intended for studying MOS electrostatics and numerical semiconductor modeling rather than predicting the complete behavior of fabricated devices.

## Possible Extensions

Possible extensions include:

* Fermi-Dirac carrier statistics
* Drift-diffusion transport
* Quantum corrections
* Interface trap modeling
* MOSFET geometry and source/drain regions
* Current-voltage characteristics
