import matplotlib.pyplot as plt


def plot_potential(out):
    x_um = out["x"] * 1e4

    plt.figure()
    plt.plot(x_um, out["psi"])
    plt.xlabel("Depth into silicon (µm)")
    plt.ylabel("Potential ψ (V)")
    plt.title("Electrostatic Potential")
    plt.grid(True)
    plt.show()


def plot_electric_field(out):
    x_um = out["x"] * 1e4

    plt.figure()
    plt.plot(x_um, out["E_si"])
    plt.xlabel("Depth into silicon (µm)")
    plt.ylabel("Electric field (V/cm)")
    plt.title("Semiconductor Electric Field")
    plt.grid(True)
    plt.show()


def plot_charge_density(out):
    x_um = out["x"] * 1e4

    plt.figure()
    plt.plot(x_um, out["rho"])
    plt.xlabel("Depth into silicon (µm)")
    plt.ylabel("Charge density ρ (C/cm³)")
    plt.title("Charge Density")
    plt.grid(True)
    plt.show()


def plot_carriers(out):
    x_um = out["x"] * 1e4

    plt.figure()
    plt.semilogy(x_um, out["n"], label="Electrons n")
    plt.semilogy(x_um, out["p"], label="Holes p")
    plt.xlabel("Depth into silicon (µm)")
    plt.ylabel("Carrier density (cm⁻³)")
    plt.title("Carrier Density Profiles")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_band_diagram(out):
    x_um = out["x"] * 1e4

    plt.figure()
    plt.plot(x_um, out["Ec"], label="Ec")
    plt.plot(x_um, out["Ei"], label="Ei")
    plt.plot(x_um, out["Ev"], label="Ev")
    plt.xlabel("Depth into silicon (µm)")
    plt.ylabel("Energy (eV)")
    plt.title("Band Diagram")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_cv(Vg, C, Cox=None):
    plt.figure()
    plt.plot(Vg, C, marker="o", markersize=3)

    if Cox is not None:
        plt.axhline(Cox, linestyle="--", label="Cox")
        plt.legend()

    plt.xlabel("Gate voltage Vg (V)")
    plt.ylabel("Capacitance (F/cm²)")
    plt.title("Quasi-static C-V Curve")
    plt.grid(True)
    plt.show()