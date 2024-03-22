import numpy.random as rand
import numpy as np

from bugs import Plankton
from simulation import init_plankton

def init_dict(initial_plankton):
    plankton_dict = {}
    for i, p in enumerate(initial_plankton):
        position_dict = {'x': [p.x], 'y': [p.y], 'y0': p.y_0, 't': [0]}
        plankton_dict[i] = position_dict
    return plankton_dict

def append_dict(plankton_dict, p, new, id, timestep):
    
    if new: # new position dict with id n_count
        position_dict = {'x': [p.x], 'y': [p.y], 'y0': p.y_0, 't': [timestep]}
        plankton_dict[id] = position_dict
        
    else: # append to exiting position dict
        plankton_dict[id]['x'].append(p.x)
        plankton_dict[id]['y'].append(p.y)
        plankton_dict[id]['t'].append(timestep)
        
    return plankton_dict
    

def run_simulation_trajectory(n: int, iterations: int, L_max: float, reproduction=True):
    delta = 10**(-3)
    k = 2*np.pi/L_max
    U_tot = 0.1 #Utot_list = [0.0, 0.1, 0.5,2.5]
    
    initial_plankton = init_plankton(n)
    plankton = initial_plankton
    reproduction_outcome = 0
    n_count = n-1

    plankton_dict = init_dict(initial_plankton)
    id_list = list(range(n))
    
    for i in range(1,iterations+1):
        # Compute the phase in x and y for the turbulent flow from Pierrehumbert. 
        # These phases are common to each particle as they correspond to a unique flow.
        phi = rand.uniform()*2*np.pi
        theta = rand.uniform()*2*np.pi
        
        new_plankton = []
        current_id = []
        #print('plankton',len(plankton))
        #print('ids',len(id_list))

        for j, id in enumerate(id_list):
            p = plankton[j]
            # Step 1. Reproduction
            if reproduction:
                reproduction_outcome = p.reproduction()

            if reproduction_outcome == 1:
                n_count += 1 # keeping track of new ids
                offspring = Plankton(p.p, p.q, p.x, p.y, p.y_0)
                
                # Step 2. Diffusion
                p.diffusion(L_max, delta)
                offspring.diffusion(L_max, delta)
                
                # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)
                offspring.advection(U_tot, k, phi, theta, L_max)

                plankton_dict = append_dict(plankton_dict=plankton_dict, p=p, new=False, id=id, timestep=i)
                current_id.append(id)
                new_plankton.append(p)

                plankton_dict = append_dict(plankton_dict=plankton_dict, p=offspring, new=True, id=n_count, timestep=i)
                current_id.append(n_count)
                new_plankton.append(offspring)
                

            elif reproduction_outcome == 0:
                # Step 2. Diffusion
                p.diffusion(L_max, delta)

                # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)

                plankton_dict = append_dict(plankton_dict=plankton_dict, p=p, new=False, id=id, timestep=i)
                current_id.append(id)
                new_plankton.append(p)

        plankton = new_plankton
        id_list = current_id

    return plankton_dict