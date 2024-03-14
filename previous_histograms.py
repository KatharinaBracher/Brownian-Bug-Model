import numpy as np

from bugs import Plankton


def pair_distance(p1: Plankton, p2: Plankton, L_max: float) -> float:
    """Calculate the Euclidean distance between two Plankton.
    
    We have to account for the periodic boundary conditions here."""
    area = L_max ** 2
    dtt2 = area

    # We need to check the 8 other squares surrounding our main square.
    # ki = -1, 0, 1.
    for ki in range(-1, 2):

        # kj = -1, 0, 1.
        for kj in range(-1, 2):
            dt2 = (p1.x - (p2.x + ki * L_max)) ** 2 + (p1.y - (p2.y + kj * L_max)) ** 2
            d2 = min(dtt2, dt2)
            dtt2 = d2

    return d2

def pair_density(plankton: list[Plankton], L_max: float, p: float, dp: float):
    n = len(plankton)
    
    area = L_max ** 2

    distances = np.zeros((n, n))

    hits = 0

    xi = 10 ** p
    dxi = 10 ** (p + dp) - xi

    for i in range(n):

        p1 = plankton[i]

        for j in range(n):

            # Only calculate the distance if the two plankton are not the same.
            if i != j:
                p2 = plankton[j]
                
                distance = pair_distance(p1, p2, L_max)

                if distance < (xi + dxi) ** 2 and distance > (xi ** 2):
                    hits += 1


    # pcf[0]=iter/(pi*(pow(xi+dxi,2.0) - pow(xi,2.0))*area)
	# pcf[1]=iter/(2*pi*log(10)*pow(10,2*p))*(1/dp)*(1/area)
                    
    pcf = hits / (np.pi * area * ((xi + dxi) ** 2 - xi ** 2))

    return distances


def compute_distances(plankton: list[Plankton], L_max: float):
    n = len(plankton)
    
    distances = np.zeros((n, n))

    for i in range(n):

        p1 = plankton[i]

        for j in range(n):

            # Only calculate the distance if the two plankton are not the same.
            if i != j:
                p2 = plankton[j]
                
                distance = pair_distance(p1, p2, L_max)

                # We only need to calculate the distances once for each pair.
                if j < i:

                    assert distance != 0

                    # pow_dist = int(max(int(-10), round(np.log10(pow(distance, 0.5)))))
                    
                    distances[i, j] = distance ** 0.5

                    # pow_dist=int(std::max(int(-10),int(round(log10(pow(d2,0.5))))));
                    #     id_pow=-1*pow_dist;
                    #     repart[id_pow]=repart[id_pow]+1;
                    #     f3<<p1<<";"<<p2<<";"<<pow(d2,0.5)<<std::endl;
                    #     }


                # distances[i, j] = pair_distance(p1, p2)

    return distances


# def PairDens(xi, dxi, particles):
#     Lmax = 1.0  # Assuming Lmax is defined elsewhere
#     area = Lmax ** 2
#     iter_count = 0
#     n = len(particles)

#     for p1 in range(n):
#         current = particles[p1]
#         for p2 in range(n):
#             if p1 != p2:
#                 temp = particles[p2]
#                 dtt2 = area
#                 for ki in range(-1, 2):
#                     for kj in range(-1, 2):
#                         dt2 = (temp.x - current.x + ki * Lmax) ** 2 + \
#                               (temp.y - current.y + kj * Lmax) ** 2
#                         d2 = min(dtt2, dt2)
#                         dtt2 = d2

#                 if xi ** 2 < d2 < (xi + dxi) ** 2:
#                     iter_count += 1

#     return iter_count / (np.pi * ((xi + dxi) ** 2.0 - xi ** 2.0) * area)


# delta = 10**(-3)
# k = 2*np.pi/L_max
# U_tot = 0.1 #Utot_list = [0.0, 0.1, 0.5,2.5]

# dxi = 10**-8

# pow_min = -1 + np.log10(delta)
# pow_max = 5 + np.log10(delta)
# dpow = 0.5 # Power increment

# pow_i = pow_min

# pcf_list = []
# xi_list = []

# while pow_i < pow_max and pow_i < 0.0:
#     print("pow", pow_i)
#     xi = 10 ** pow_i
#     pow_i += dpow
#     C = len(plankton) / area
#     pcf = PairDens(xi, dxi, plankton) / (C ** 2)
#     print(pcf)

#     xi_list.append(xi / delta)
#     pcf_list.append(pcf)