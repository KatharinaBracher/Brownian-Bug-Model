import numpy.random as rand
import numpy as np
from copy import deepcopy

from bugs import Plankton
from simulation import init_plankton

def get_pos(plankton_obj):
    x = [p.x for p in plankton_obj]
    y = [p.y for p in plankton_obj]
    starting_positions_0 = [p.y_0 for p in plankton_obj]
    return x,y,starting_positions_0

def append_pos(x_pos, y_pos, starting_pos, plankton_obj):
    x,y,starting_positions_0 = get_pos(plankton_obj)
    x_pos.append(x)
    y_pos.append(y)
    starting_pos.append(starting_positions_0)

def run_simulation_animation(n: int, iterations: int, L_max: float, reproduction=True):
    #rng = rand.default_rng()
    #positions = np.zeros((n, 2, iterations))
    x_pos = []
    y_pos = []
    starting_pos = []

    delta = 10**(-3)
    k = 2*np.pi/L_max
    U_tot = 0.1 #Utot_list = [0.0, 0.1, 0.5,2.5]
    
    initial_plankton = init_plankton(n)
    plankton = initial_plankton
    reproduction_outcome = 0

    append_pos(x_pos, y_pos, starting_pos, plankton)
    
    for i in range(iterations):
        # Compute the phase in x and y for the turbulent flow from Pierrehumbert. 
        # These phases are common to each particle as they correspond to a unique flow.
        phi = rand.uniform()*2*np.pi
        theta = rand.uniform()*2*np.pi
        
        new_plankton = []

        for j, p in enumerate(plankton):
            # Step 1. Reproduction
            if reproduction:
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
        append_pos(x_pos, y_pos, starting_pos, plankton)

    return x_pos, y_pos, starting_pos