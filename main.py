import numpy as np
import random


class sys():
    def __init__(self, n_side):
        self.n_side = n_side
        self.K = 0.1 #J/kT
        self.lattice = np.zeros(shape=(n_side,n_side))

    def initialize(self, param):
        if param.lower() == 'ordered':
            for i in range(self.n_side):
                for j in range(self.n_side):
                    self.lattice[i][j] = 1

        elif param.lower() == 'disordered':
            for i in range(self.n_side):
                for j in range(self.n_side):
                    self.lattice[i][j] = np.random.randint(0,2) * 2 - 1
        
        else:
            print("System must be initialized to either 'ordered', or 'disordered'")
            pass

        self.E, self.M = self.calculate_energy()
        
    def site_energy(self,i,j):
        """
        Calculates betaE for one site, [i][j], in the two-dimensional Ising Model
        """
        left = (i - 1) % self.n_side
        right = (i + 1) % self.n_side
        up = (j + 1) % self.n_side
        down = (j - 1) % self.n_side
        neighbors = self.lattice[left][j] + self.lattice[right][j] + self.lattice[i][up] + self.lattice[i][down]

        en = -self.K * self.lattice[i][j] * neighbors
        return en

    def calculate_energy(self):
        """
        Calculates the total energy and magnetization of the system
        """
        E = 0
        M = 0

        for i in range(self.n_side):
            for j in range(self.n_side):
                E += self.site_energy(i,j)
                M += self.lattice[i][j]

        return E, M

def traj(sys, steps, sample_freq):
    size = floor(steps / sample_freq)
    trajectory = np.zeros(shape(size,1))
    for i in range(steps):
        #sys = metropolis(sys)
        if i % sample_freq == 0:
            traj[count] = sys.lattice

def metropolis(sys):
    i = random.randrange(sys.n_side)
    j = random.randrange(sys.n_side)
    de = delta_e(sys, i, j)

    accept = False
    if de <= 0:
        accept = True
    else:
        if(random.random() < np.exp(-de)):
            accept = True

    if accept:
        sys.lattice[i][j] *= -1
        sys.E += de
        sys.M += 2 * sys.lattice[i][j]

def delta_e(sys, i, j):
    de = -2 * sys.site_energy(i,j)
    return de

def trajectory(sys, steps, sample_freq):
    traj = dict()
    count = 0
    for i in range(steps):
        metropolis(sys)
        if i % sample_freq == 0:
            sample = {'Energy': sys.E, 'Magnetization': sys.M, 'Lattice': sys.lattice}
            traj[count] = sample
            count += 1
    return traj



S = sys(n_side=5)
print('Zero lattice: ')
print(S.lattice)

S.initialize('ordered')
print('Initialized lattice: ')
print(S.lattice)

print(f'Initial energy: {S.E}\nInitial magnetization: {S.M}')

n_steps = 100
for _ in range(n_steps):
    metropolis(S)

print(f'Lattice after {n_steps} steps:')
print(S.lattice)
print(f'Final energy: {S.E}\nFinal magnetization: {S.M}')

import pprint
traj = trajectory(S, 100, 10)
pprint.pprint(traj)
