import numpy as np
from bugs import Plankton
from scipy.special import expi
from scipy.stats import linregress
import numpy.random as rand
#from trajectory import init_dict, append_dict

def init_plankton(n: int, L_max: float, p: float = 0.5, q:float = 0.5):
    x_lim = L_max
    y_lim = L_max

    x_init_positions = np.random.rand(n) * x_lim
    y_init_positions = np.random.rand(n) * y_lim

    plankton = [Plankton(p, q, x_init_positions[i], y_init_positions[i]) for i in range(n)]

    return plankton

def init_dict_PC(initial_plankton):
    plankton_dict = {}
    for i, p in enumerate(initial_plankton):
        position_dict = {'x': [p.x], 'y': [p.y], 'y0': p.y_0, 't': [0], 'childs': []}
        plankton_dict[i] = position_dict
    return plankton_dict

def append_dict_PC(plankton_dict, p, new, id, timestep):
    
    if new: # new position dict with id n_count
        position_dict = {'x': [p.x], 'y': [p.y], 'y0': p.y_0, 't': [timestep], 'childs': []}
        plankton_dict[id] = position_dict
        
    else: # append to exiting position dict
        plankton_dict[id]['x'].append(p.x)
        plankton_dict[id]['y'].append(p.y)
        plankton_dict[id]['t'].append(timestep)

    return plankton_dict

def run_simulation_trajectory_PC(n: int, iterations: int, U_tot: float, L_max: float, reproduction=True):

    delta = 0.0
    k = 2*np.pi/L_max
    
    initial_plankton = init_plankton(n,L_max)
    plankton = initial_plankton
    reproduction_outcome = 0
    n_count = n-1

    plankton_dict = init_dict_PC(initial_plankton)
    id_list = list(range(n))
    av_log_dist = [np.log(10**(-7))]

    phi = rand.uniform()*2*np.pi
    theta = rand.uniform()*2*np.pi
        
    new_plankton = []
    current_id = []
    distances=[]

    for j, id in enumerate(id_list):
        p = plankton[j]
        # Step 1. Reproduction
        if reproduction:
            reproduction_outcome = p.reproduction()

        if reproduction_outcome == 1:
            n_count += 1 # keeping track of new ids
            offspring = Plankton(p.p, p.q, p.x, p.y+10**(-7), p.y_0)

            for _ in range(1):
                
            # Step 2. Diffusion
                p.diffusion(L_max, delta)
                offspring.diffusion(L_max, delta)
                
            # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)
                offspring.advection(U_tot, k, phi, theta, L_max)

            plankton_dict = append_dict_PC(plankton_dict=plankton_dict, p=p, new=False, id=id, timestep=1)
            current_id.append(id)
            new_plankton.append(p)
            plankton_dict[id]['childs'].append(n_count)

            plankton_dict = append_dict_PC(plankton_dict=plankton_dict, p=offspring, new=True, id=n_count, timestep=1)
            current_id.append(n_count)
            new_plankton.append(offspring)
                

        elif reproduction_outcome == 0:
            # Step 2. Diffusion
            p.diffusion(L_max, delta)

            # Step 3. Advection
            p.advection(U_tot, k, phi, theta, L_max)

            plankton_dict = append_dict_PC(plankton_dict=plankton_dict, p=p, new=False, id=id, timestep=1)
            current_id.append(id)
            new_plankton.append(p)

    plankton = new_plankton
    id_list = current_id

    for i in range(1,iterations):
        # Compute the phase in x and y for the turbulent flow from Pierrehumbert. 
        # These phases are common to each particle as they correspond to a unique flow.
        phi = rand.uniform()*2*np.pi
        theta = rand.uniform()*2*np.pi
        new_plankton = []
        current_id = []
        distances=[]

        for j, id in enumerate(id_list):
            p = plankton[j]
                
            # Step 2. Diffusion
            if U_tot == 0.5 or U_tot == 2.5:
                s = 2
            else:
                s=1
            for _ in range(s):
                p.diffusion(L_max, delta)
                
            # Step 3. Advection
                p.advection(U_tot, k, phi, theta, L_max)

            plankton_dict = append_dict_PC(plankton_dict=plankton_dict, p=p, new=False, id=id, timestep=i)
            current_id.append(id)
            new_plankton.append(p)

        plankton = new_plankton
        id_list = current_id

        for j in range(len(plankton_dict)):
            p = plankton_dict[j]
            px = p['x'][-1]
            py = p['y'][-1]
            children_list = p['childs']
            if children_list != []:
                for indices in children_list:
                    child = plankton_dict[indices]
                    childx = child['x'][-1]
                    childy = child['y'][-1]
                    dx = min(np.abs(px - childx), L_max - np.abs(px - childx))
                    dy = min(np.abs(py - childy), L_max - np.abs(py - childy))
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance == 0:
                        distance = 10**(-9)
                    distances.append(distance)

                
        av_log_dist.append(np.mean(np.log(np.array(distances)))) 
                          

    return av_log_dist


def find_gamma(n, U_tot, L_max):
    """ Plankton dictionary found for a certian value of U_tot, calculate
    pairwise distances between parents and children at each time step
    Return the slope of average logarithm of distances with time
    """

    if U_tot == 0.5:
        iters = 15
    elif U_tot == 2.5:
        iters = 4
    else:
        iters = 100

    av_log_dist = run_simulation_trajectory_PC(n, iters, U_tot, L_max, True)
        
    
    tmax = len(av_log_dist)
    t = list(range(0,tmax))
    gamma = linregress(t, 0.5*np.array(av_log_dist))[0]

    return gamma, 0.5*np.array(av_log_dist), t

