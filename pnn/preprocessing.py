"""
Data preprocessing tools.
"""

import numpy as np


def load_training_data(file, N=np.inf):
    data = np.empty([4, 2])
    with open(file, 'rb') as f:
        while True:
            try:
                # Load the next array and append it to the list
                loaded_array = np.load(f)
                data = np.row_stack((data,loaded_array))
                print('load', loaded_array.shape)
                if data.shape[0]>=N:
                    break
            except EOFError:
                # End of file reached
                break
    if N<np.inf: 
        data = data[:N]
    return data

class Scaler:
    """
    Class for scaling data by standardisation. Includes methods for inverting
    the scaling of data and related probability densities, means and
    covariances.
    """

    def __init__(self, X):
        assert len(X.shape) > 1, "X must have dimension greater than 1."
        self.mean = X.mean(axis=0)
        self.std = X.std(axis=0)

    def standardise(self, X):
        return (X - self.mean) / self.std

    def invert_standardisation(self, X):
        return (X * self.std) + self.mean

    def invert_standardisation_prob(self, prob):
        return prob / self.std.prod()

    def invert_standardisation_log_prob(self, prob):
        return prob - np.log(self.std.prod())

    def invert_standardisation_loc(self, loc):
        return self.invert_standardisation(loc)

    def invert_standardisation_cov(self, cov):
        return cov * (self.std[:, None] @ self.std[None, :])


