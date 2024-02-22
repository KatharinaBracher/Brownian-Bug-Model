import numpy as np

from bugs import Plankton


def init_plankton(n: int):
    x_lim = 1
    y_lim = 1

    x_init_positions = np.random.rand(n) * x_lim
    y_init_positions = np.random.rand(n) * y_lim

    p = 0.5
    q = 0.5

    plankton = [Plankton(p, q, x_init_positions[i], y_init_positions[i]) for i in range(n)]

    return plankton


def run_simulation(n: int, iterations: int, L_max: float):
    plankton = init_plankton(n)

    positions = np.zeros((n, 2, iterations))

    delta = 0.1

    for i in range(iterations):

        for j, p in enumerate(plankton):

            # Step 2. Diffusion
            p.diffusion(L_max, delta)

            # Step 3. Advection
            # p.advection()

            positions[j, :, i] = p.get_coords()

    return plankton, positions


def pair_distance(p1: Plankton, p2: Plankton) -> float:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2
