import numpy.random as rand
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
    #rng = rand.default_rng()
    positions = np.zeros((n, 2, iterations))

    delta = 10**(-3)
    k = 2*np.pi/L_max
    U_tot = 0.1 #Utot_list = [0.0, 0.1, 0.5,2.5]
    
    plankton = init_plankton(n)
    
    for i in range(iterations):
        # Compute the phase in x and y for the turbulent flow from Pierrehumbert. 
        # These phases are common to each particle as they correspond to a unique flow.
        phi = rand.uniform()*2*np.pi
        theta = rand.uniform()*2*np.pi
        
        for j, p in enumerate(plankton):
            # Step 1. Reproduction
            

            # Step 2. Diffusion
            p.diffusion(L_max, delta)

            # Step 3. Advection
            p.advection(U_tot, k, phi, theta, L_max)

            positions[j, :, i] = p.get_coords()

    return plankton, positions


def pair_distance(p1: Plankton, p2: Plankton) -> float:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2
