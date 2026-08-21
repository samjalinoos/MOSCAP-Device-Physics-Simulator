import numpy as np

from physics.solver import solve_moscap
from analysis.postprocess import postprocess_solution

def sweep_gate_voltage(Vg_values, device, x, dx):
    results = []

    psi_guess = None

    for Vg in Vg_values:
        psi, solver_result = solve_moscap(
            Vg=Vg,
            device=device,
            x=x,
            dx=dx,
            psi_guess=psi_guess,
        )

        if not solver_result.success:
            raise RuntimeError(f"Solver failed at Vg={Vg}: {solver_result.message}")

        out = postprocess_solution(x, dx, psi, device, Vg)
        out["Vg"] = Vg
        out["solver_success"] = solver_result.success
        out["solver_message"] = solver_result.message

        results.append(out)

        psi_guess = psi

    return results


def extract_cv(results):
    Vg = np.array([r["Vg"] for r in results])
    Qg = np.array([r["Qg"] for r in results])
    C = np.gradient(Qg, Vg)

    return Vg, Qg, C