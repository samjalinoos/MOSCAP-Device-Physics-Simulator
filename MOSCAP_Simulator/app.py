import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from physics.device import MOSCAPDevice
from physics.grid import make_grid
from physics.solver import solve_moscap
from analysis.postprocess import postprocess_solution
from styles import load_css

PRESETS = {
    "P-type baseline": {"substrate_type": "p", "doping": 1e16, "T": 300.0, "tox_nm": 10.0, "oxide_k": 3.9, "phi_m": 4.1},
    "N-type baseline": {"substrate_type": "n", "doping": 1e16, "T": 300.0, "tox_nm": 10.0, "oxide_k": 3.9, "phi_m": 4.1},
    "Thin oxide": {"substrate_type": "p", "doping": 1e16, "T": 300.0, "tox_nm": 2.0, "oxide_k": 3.9, "phi_m": 4.1},
    "Heavy doping": {"substrate_type": "p", "doping": 1e18, "T": 300.0, "tox_nm": 10.0, "oxide_k": 3.9, "phi_m": 4.1},
    "High-k oxide": {"substrate_type": "p", "doping": 1e16, "T": 300.0, "tox_nm": 10.0, "oxide_k": 20.0, "phi_m": 4.1},
}

DOPING_OPTIONS = {
    "1e14": 1e14,
    "1e15": 1e15,
    "1e16": 1e16,
    "1e17": 1e17,
    "1e18": 1e18,
    "1e19": 1e19,
}

REGIME_EXPLANATIONS = {
    "Flat Band": "Surface charge is approximately zero and the semiconductor bands remain largely unbent.",
    "Accumulation": "Positive surface charge attracts majority carriers toward the interface, increasing carrier concentration near the oxide boundary.",
    "Depletion": "Majority carriers are repelled from the surface, exposing ionized dopants and forming a depletion region.",
    "Strong Inversion": "Minority carriers dominate the surface region, creating an inversion layer capable of supporting MOSFET channel conduction.",
}


st.set_page_config(
    page_title="MOSCAP Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

with st.sidebar:
    st.header("Example Device")

    preset_name = st.selectbox("Preset", list(PRESETS.keys()))
    preset = PRESETS[preset_name]

    st.header("Device Parameters")

    substrate_type = st.selectbox(
        "Semiconductor Type",
        ["p", "n"],
        index=["p", "n"].index(preset["substrate_type"]),
    )

    doping_keys = list(DOPING_OPTIONS.keys())
    preset_doping_key = f"{preset['doping']:.0e}".replace("+", "")

    doping_label = st.selectbox(
        "Doping Concentration (cm⁻³)",
        doping_keys,
        index=doping_keys.index(preset_doping_key),
    )

    doping = DOPING_OPTIONS[doping_label]

    T = st.number_input("Device Temperature [K]", value=preset["T"])
    tox_nm = st.number_input("Oxide Thickness [nm]", value=preset["tox_nm"])
    oxide_k = st.number_input("Relative Oxide Permittivity (k)", value=preset["oxide_k"])
    phi_m = st.number_input("Gate Work Function Φm [eV]", value=preset["phi_m"])

    Qox = 0.0

    st.header("Bias")

    Vg_offset = st.slider(
        "Effective Gate Bias: Vg - Vfb [V]",
        -2.0,
        2.0,
        0.0,
        0.01,
    )

    st.header("Numerical Grid")

    L_um = st.number_input("Simulation Depth [μm]", value=1.0)

    num_points = st.slider(
        "Numerical Grid Points",
        51,
        801,
        201,
        step=50,
    )


device = MOSCAPDevice(
    substrate_type=substrate_type,
    doping=doping,
    T=T,
    tox_cm=tox_nm * 1e-7,
    oxide_k=oxide_k,
    phi_m=phi_m,
    Qox=Qox,
)

x, dx = make_grid(L_cm=L_um * 1e-4, num_points=num_points)
Vg = device.Vfb + Vg_offset

psi, result = solve_moscap(Vg, device, x, dx)
out = postprocess_solution(x, dx, psi, device, Vg)

x_um = x * 1e4


st.markdown(
    """
    <div class="title-card">
        <h1>MOSCAP Device Physics Simulator</h1>
        <div style="color:#aeb8c7; font-size:1.02rem;">
            A 1D MOS capacitor simulator written in Python. 
            It solves the nonlinear Poisson-Boltzmann equation to model electrostatic potential, carrier concentrations, 
            charge density, electric field, and band bending as a function of gate bias.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-label">Device State</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Regime", out["regime"])
m2.metric("Effective Gate Bias", f"{Vg_offset:.3f} V")
m3.metric("Surface Potential ψs", f"{out['psi_s']:.3f} V")
m4.metric("Flat-Band Voltage Vfb", f"{device.Vfb:.4f} V")

m5, m6, m7 = st.columns(3)
m5.metric("Strong Inversion Threshold 2φF", f"{2 * device.phi_f:.4f} V")
m6.metric("Surface Electron Density", f"{out['n_surface']:.3e} cm⁻³")
m7.metric("Surface Hole Density", f"{out['p_surface']:.3e} cm⁻³")

st.info(REGIME_EXPLANATIONS.get(out["regime"], ""))


def plot_line(y, ylabel, title, logy=False):
    fig, ax = plt.subplots(figsize=(7, 3.55), facecolor="#0b1020")
    ax.set_facecolor("#111827")

    ax.plot(x_um, y, linewidth=2.0)

    ax.set_xlabel("Depth into silicon [μm]", color="#d1d5db")
    ax.set_ylabel(ylabel, color="#d1d5db")
    ax.set_title(title, color="#f9fafb", pad=10, fontsize=13, fontweight="bold")

    if logy:
        ax.set_yscale("log")

    ax.grid(True, alpha=0.22)
    ax.tick_params(colors="#d1d5db")

    for spine in ax.spines.values():
        spine.set_color("#374151")

    st.pyplot(fig, use_container_width=True)


st.divider()
st.markdown('<div class="section-label">Solved Profiles</div>', unsafe_allow_html=True)

electro_tab, carrier_tab, band_tab = st.tabs(
    ["Electrostatics", "Carriers + Charge", "Band Diagram"]
)

with electro_tab:
    col1, col2 = st.columns(2)

    with col1:
        plot_line(
            out["psi"],
            "ψ [V]",
            "Electrostatic Potential ψ(x)",
        )

    with col2:
        plot_line(
            out["E_si"],
            "E [V/cm]",
            "Electric Field E(x)",
        )

with carrier_tab:
    col1, col2 = st.columns(2)

    with col1:
        plot_line(
            out["rho"],
            "ρ [C/cm³]",
            "Space Charge Density ρ(x)",
        )

    with col2:
        fig, ax = plt.subplots(figsize=(7, 3.55), facecolor="#0b1020")
        ax.set_facecolor("#111827")

        ax.plot(x_um, out["n"], label="n electrons", linewidth=2.0)
        ax.plot(x_um, out["p"], label="p holes", linewidth=2.0)

        ax.set_yscale("log")
        ax.set_xlabel("Depth into silicon [μm]", color="#d1d5db")
        ax.set_ylabel("Carrier density [cm⁻³]", color="#d1d5db")
        ax.set_title("Carrier Densities", color="#f9fafb", pad=10, fontsize=13, fontweight="bold")

        ax.legend(facecolor="#111827", edgecolor="#374151", labelcolor="#e5e7eb")
        ax.grid(True, alpha=0.22)
        ax.tick_params(colors="#d1d5db")

        for spine in ax.spines.values():
            spine.set_color("#374151")

        st.pyplot(fig, use_container_width=True)

with band_tab:
    fig, ax = plt.subplots(figsize=(9, 4.2), facecolor="#0b1020")
    ax.set_facecolor("#111827")

    ax.plot(x_um, out["Ec"], label="Ec", linewidth=2.0)
    ax.plot(x_um, out["Ei"], label="Ei", linewidth=2.0)
    ax.plot(x_um, out["Ev"], label="Ev", linewidth=2.0)

    ax.set_xlabel("Depth into silicon [μm]", color="#d1d5db")
    ax.set_ylabel("Energy [eV]", color="#d1d5db")
    ax.set_title("Band Bending from Solved Potential", color="#f9fafb", pad=10, fontsize=13, fontweight="bold")

    ax.legend(facecolor="#111827", edgecolor="#374151", labelcolor="#e5e7eb")
    ax.grid(True, alpha=0.22)
    ax.tick_params(colors="#d1d5db")

    for spine in ax.spines.values():
        spine.set_color("#374151")

    st.pyplot(fig, use_container_width=True)