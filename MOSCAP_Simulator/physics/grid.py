import numpy as np


def make_grid(L_cm, num_points):
    if L_cm <= 0:
        raise ValueError("L_cm must be positive")

    if num_points < 3:
        raise ValueError("num_points must be at least 3")

    x = np.linspace(0.0, L_cm, num_points)
    dx = x[1] - x[0]

    return x, dx