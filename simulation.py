import numpy.random as rand
import numpy as np

from bugs import Plankton


def init_plankton(n: int, p: float = 0.5, q:float = 0.5):
    x_lim = 1
    y_lim = 1

    x_init_positions = np.random.rand(n) * x_lim
    y_init_positions = np.random.rand(n) * y_lim

    plankton = [Plankton(p, q, x_init_positions[i], y_init_positions[i]) for i in range(n)]

    return plankton


def run_simulation(n: int, iterations: int, L_max: float, reproduction=True):
    #rng = rand.default_rng()
    #positions = np.zeros((n, 2, iterations))

    delta = 10**(-3)
    k = 2*np.pi/L_max
    U_tot = 0.1 #Utot_list = [0.0, 0.1, 0.5,2.5]
    
    initial_plankton = init_plankton(n)
    plankton = initial_plankton
    reproduction_outcome = 0
    
    for i in range(iterations):
        # Compute the phase in x and y for the turbulent flow from Pierrehumbert. 
        # These phases are common to each particle as they correspond to a unique flow.
        phi = rand.uniform()*2*np.pi
        theta = rand.uniform()*2*np.pi
        
        new_plankton = []

        for j, p in enumerate(plankton):
            # Step 1. Reproduction
            if reproduction:
                reproduction_outcome = p.reproduction() #either 1 or -1

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
            #if reproduction_outcome == -1 the plankton has died

            # no reproduction
            elif reproduction_outcome == 0:
                # Step 2. Diffusion
                p.diffusion(L_max, delta)

                # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)

                new_plankton.append(p)

            #positions[j, :, i] = p.get_coords()
        plankton = new_plankton

    return plankton, initial_plankton
