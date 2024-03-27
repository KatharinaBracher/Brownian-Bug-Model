"""
This file implements the histogram modelling process and is intended to be used for running on Eddie.
"""

import numpy as np
from histograms import PairDens, run_simulation, g_theoretical
from concurrent.futures import ProcessPoolExecutor

Utot_list = [0.0, 0.1, 0.5, 2.5]
gamma_list = [-2.82*10**(-15), 0.0264, 0.506, 2.43]

Utot_gamma_pairs = list(zip(Utot_list, gamma_list))

n = 200000 # Starting plankton population size.
iters = 1000 # Time steps.
L_max = np.sqrt(10) # Size of square domain.
area = L_max**2
delta = 10**(-7)
pow_min = -8.0 # To reproduce the image, choose -8.0
pow_max = -1.5 # To reproduce the image, choose -1.5
dp = 0.25

def simulation_for_Utot(U_tot_gamma):
    U_tot, gamma = U_tot_gamma
    plankton = run_simulation(n, iters, L_max, delta, U_tot, True)
    print(f"Number of plankton after the simulation for {U_tot}: {len(plankton)}.")
    
    edges, pcf_dx, pcf_dp = PairDens(pow_min, pow_max, dp, L_max, plankton)

    radii = [i / delta for i in edges]

    C_0 = len(plankton) / area

    g_test = g_theoretical(gamma, radii, C_0, iters)
    
    return radii, pcf_dx, pcf_dp, g_test

with ProcessPoolExecutor() as executor:
    results = list(executor.map(simulation_for_Utot, Utot_gamma_pairs))
    np.save("results_histograms.npy", results)