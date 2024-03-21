import numpy as np
from bugs import Plankton


def pair_distance(p1: Plankton, p2: Plankton, L_max: float) -> float:
    """Calculates the Euclidean distance between two Plankton.

    We have to account for the periodic boundary conditions here.
    
    Input:
        p1: first plankton with positions x and y.
        p2: second plankton with positions x and y
        L_max: the size of the domain along one dimension (given a squared domain).
    
    Output:
        The minimum distance between p1 and p2 considering periodic boundaries.
    """

    # We calculate the distance between two individual plankton
    dx = np.abs(p1.x - p2.x)
    dy = np.abs(p1.y - p2.y)

    # We account for the periodic boundary conditions
    dx = min(np.abs(p1.x - p2.x), L_max - np.abs(p1.x - p2.x))
    dy = min(np.abs(p1.y - p2.y), L_max - np.abs(p1.y - p2.y))

    # We compute the Euclidean distance between the two plankton
    distance = np.sqrt(dx**2 + dy**2)

    return distance


def PairDens(pow_min, pow_max, dp, L_max, plankton):
    """Function that computes pair densities within a population of plankton.
    
    INPUTS:
        pow_min: base 10 logarithm of the starting radius for which we want to calculate the pair density.
        pow_max: base 10 logarithm of the final radius for which we want to calculate the pair density.
        dp: increment in the power of 10 to define the range (or "bin") for the distances over which to calculate the pair density.
        L_max: size of one side of the square domain.
        plankton: list containing all the current plankton.

    OUTPUT:
        pcf_dx: measure of pair density.
        pcf_dp: measure of pair density normalised in a different way.
    """

    # We calculate the edges of the bins for the histogram.
    edges = 10 ** np.arange(pow_min, pow_max + dp, dp)

    # We initialise the count of particle pairs.
    counts = np.zeros(len(edges) - 1)
    
    # We initialise a list to store all pairwise distances.
    distances = []

    # We iterate over all unique pairs of plankton. We take (i + 1) in the second loop to avoid repetitions.
    for i in range(len(plankton)):
        for j in range(i + 1, len(plankton)):
            # We calculate the distance between the pair.
            distance = pair_distance(plankton[i], plankton[j], L_max)

            # We append the computed distance to our list of distances.
            distances.append(distance)
                
    # We convert our list of distances into an array.
    distances = np.array(distances)

    # We assign each distance to a specific bin.
    bins = np.digitize(distances, edges)

    # We count the number of occurrences in each bin.
    for index in bins:
        if 0 < index < len(edges):
            counts[index - 1] += 1
    
    pcf_dx_list = []
    pcf_dp_list = []

    for i in range(len(counts)):
        xi = edges[i]
        dxi = edges[i + 1] - xi

        # We compute the area of the annulus in order to normalise the count of the pairs.
        annular_area = np.pi * ((xi + dxi) ** 2 - xi ** 2)

        # We calculate the concentration of plankton in the given annulus.
        pcf_dx = counts[i] / annular_area

        # We calculate the concentration of plankton for logarithmic scaling.
        pcf_dp = counts[i] / (2 * np.pi * xi * dxi * np.log(10))

        pcf_dx_list.append(pcf_dx)
        pcf_dp_list.append(pcf_dp)
    
    return edges[:-1], pcf_dx_list, pcf_dp_list



# Theoretical value of g
n = 500
C_0 = n/10
gamma = 0.0264

def g_theoretical(gamma, rDelta, C_0):
    tau = 1
    lamda = 0.5
    Delta = 10**(-7)
    if gamma >0: # assuming advection U>0
        tmp = -1*lamda*tau/(2*np.pi*C_0*Delta**2)*(np.log(gamma)-np.log(1/(tau*np.array(rDelta)**2)+gamma))
    else: # case without advection
        D = Delta**2/(2*tau)
        tmax = iters*tau
        tmp = 2*lamda/C_0 * (scipy.special.exp1((np.array(rDelta)*Delta)**2/(8*tmax*D))/(8*np.pi*D))
        
    return tmp