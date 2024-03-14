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


def PairDens(p, dp, L_max, plankton):
    """Function that computes pair densities within a population of plankton.
    
    INPUTS:
        p: base 10 logarithm of the starting radius for which we want to calculate the pair density.
        dp: increment in the power of 10 to define the range (or "bin") for the distances over which to calculate the pair density.
        L_max: size of one side of the square domain.
        plankton: list containing all the current plankton.

    OUTPUT:
        pcf_dx: measure of pair density.
        pcf_dp: measure of pair density normalised in a different way.
    """

    # We calculate the starting radius.
    xi = 10 ** p

    # We calculate the width of the annular area that will be incrementing our radius.
    dxi = 10 ** (p + dp) - xi

    # We initialise the count of particle pairs.
    count = 0
    
    # We iterate over all unique pairs of plankton. We take (i + 1) in the second loop to avoid repetitions.
    for i in range(len(plankton)):
        for j in range(i + 1, len(plankton)):
            # We calculate the distance between the pair.
            distance = pair_distance(plankton[i], plankton[j], L_max)

            # If the particle is in the annular area, we add one to the total count of particle pairs.
            if xi < distance <= xi + dxi:
                count += 1
                
                
    # We compute the area of the annulus in order to normalise the count of the pairs.
    annular_area = np.pi * ((xi + dxi) ** 2 - xi ** 2)

    # We calculate the concentration of plankton in the given annulus.
    pcf_dx = count / annular_area

    # We calculate the concentration of plankton for logarithmic scaling.
    pcf_dp = count / (2 * np.pi * xi * dxi * np.log(10))
    
    return pcf_dx, pcf_dp