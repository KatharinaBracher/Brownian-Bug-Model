import numpy.random as rand

class Plankton:

    def __init__(self, p: float, q: float, x: float, y: float):
        """
        p: reproduction rate.
        q: death rate.
        x: initial x position.
        y: initial y position.
        """
        # Probability of reproduction.
        self.p = p

        # Probability of death.
        self.q = q

        # Position.
        self.x = x
        self.y = y

        # Record the initial y position for plotting.
        self.x_0 = x
        self.y_0 = y

        self.rand = rand.default_rng() 

    def get_coords(self):
        return self.x, self.y

    def reproduction(self):
        r = self.rand.uniform()
        if r < self.p:
            return 1
        elif r < self.p + self.q:
            return -1
        return 0
    
    def advection(self, U_tot: float, k: float, phi: float, theta: float, L_max: float):
        """Pierre-Humbert Flow."""
        self.check_boundaries(L_max)

    def diffusion(self, L_max: float, delta: float):
        d_x = self.rand.normal(scale=delta)
        d_y = self.rand.normal(scale=delta)
        self.x += d_x
        self.y += d_y
        self.check_boundaries(L_max)

    def check_boundaries(self, L_max: float) -> None:
        if self.x > L_max:
            self.x -= L_max
        elif self.x < 0:
            self.x += L_max
        elif self.y > L_max:
            self.y -= L_max
        elif self.y < 0 :
            self.y += L_max
        return
