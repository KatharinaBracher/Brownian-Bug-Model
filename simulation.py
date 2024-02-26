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
    #positions = np.zeros((n, 2, iterations))

    delta = 10**(-3)
    k = 2*np.pi/L_max
    U_tot = 0.1 #Utot_list = [0.0, 0.1, 0.5,2.5]
    
    initial_plankton = init_plankton(n)
    plankton = initial_plankton
    
    for i in range(iterations):
        # Compute the phase in x and y for the turbulent flow from Pierrehumbert. 
        # These phases are common to each particle as they correspond to a unique flow.
        phi = rand.uniform()*2*np.pi
        theta = rand.uniform()*2*np.pi
        
        new_plankton = []

        for j, p in enumerate(plankton):
            # Step 1. Reproduction
            reproduction_outcome = p.reproduction()

            if reproduction_outcome == 1:
                offspring = Plankton(p.p, p.q, p.x, p.y, p.y_0)
                
                # Step 2. Diffusion
                p.diffusion(L_max, delta)
                offspring.diffusion(L_max, delta)
                
                # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)
                offspring.advection(U_tot, k, phi, theta, L_max)
                
                new_plankton.append(offspring)
                new_plankton.append(p)

            elif reproduction_outcome == 0:
                # Step 2. Diffusion
                p.diffusion(L_max, delta)

                # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)

                new_plankton.append(p)

            #positions[j, :, i] = p.get_coords()
        plankton = new_plankton

    return plankton, initial_plankton


def pair_distance(p1: Plankton, p2: Plankton) -> float:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2
