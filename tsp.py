import numpy as np
from copy import deepcopy
from sys import stdin, argv

class TSP:
    def __init__(self,
                 distance_matrix):
        self.n_dimensions = len(distance_matrix)
        self.distances = distance_matrix
        
    def initialize_particles(self):
        self.particles = []
        particle_set = set()
        while len(self.particles) < self.n_particles:
            particle = np.random.permutation(self.n_dimensions)
            hash = str(particle)
            if hash not in particle_set:
                particle_set.add(hash)
                self.particles.append(particle)
        self.particles = np.array(self.particles)

    def solve_PSO(self,
                  n_particles,
                  max_iterations,
                  uncertainty):
        self.n_particles = n_particles
        self.max_iterations = max_iterations
        self.uncertainty = deepcopy(uncertainty)

        self.initialize_particles()
        self.pbest = self.particles.copy()
        self.gbest = min(self.particles, key = lambda s : self.fitness(s))

        print(self.n_particles)
        for _ in range(self.max_iterations):
            for i in range(self.n_particles):
                fit = self.fitness(self.particles[i])
                if fit < self.fitness(self.pbest[i]):
                    self.pbest[i] = self.particles[i]
                if fit < self.fitness(self.gbest):
                    self.gbest = self.particles[i]
            for i in range(self.n_particles):
                self.update(i)
                print(self.fitness(self.pbest[i]))
            print(self.fitness(self.gbest))

            self.uncertainty[0] *= 0.95
            self.uncertainty[1] *= 1.01
            self.uncertainty[2] = 1-(self.uncertainty[0]+self.uncertainty[1])

        return self.gbest, self.fitness(self.gbest)
    
    def update(self, i):
        c0 = np.random.rand(1)
        c1 = np.random.rand(1)*(1-c0)
        c2 = 1-(c0+c1)
        c3 = np.random.rand(1)
        
        if c0 < self.uncertainty[0]: self.local_search(i)
        if c1 < self.uncertainty[1]: self.path_relink(i, self.pbest[i])
        if c2 < self.uncertainty[2]: self.path_relink(i, self.gbest)
        if c3 < self.uncertainty[3]: 
            j = np.random.randint(self.n_dimensions)            
            k = np.random.randint(self.n_dimensions)
            self.particles[i][j], self.particles[i][k] = \
                self.particles[i][k], self.particles[i][j]

    def local_search(self, i):
        neighborhood = self.get_neighborhood(self.particles[i])
        best_neighbor = neighborhood[0]
        for neighbor in neighborhood:
            if self.fitness(neighbor) < self.fitness(best_neighbor):
                best_neighbor = neighbor

        self.particles[i] = best_neighbor

    def path_relink(self, i, target):
        best_neighbor = self.particles[i].copy()
        pivot = np.where(self.particles[i] == target[0])[0][0]

        self.particles[i] = np.array([
            self.particles[i][(j+pivot)%self.n_dimensions] 
            for j in range(self.n_dimensions)])
        
        for j in range(1,self.n_dimensions):
            pivot = np.where(self.particles[i] == target[j])[0][0]
            for k in range(pivot,j-1,-1):
                self.particles[i][k], self.particles[i][k-1] = \
                    self.particles[i][k-1], self.particles[i][k]
                if self.fitness(self.particles[i]) < self.fitness(best_neighbor):
                    best_neighbor = self.particles[i].copy()

        self.particles[i] = best_neighbor

    def get_neighborhood(self, s):
        neighborhood = []
        for i in range(self.n_dimensions):
            for j in range(i+1, self.n_dimensions):
                neighbor = s.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighborhood.append(neighbor)
        return neighborhood

    def fitness(self, s):
        pair_distances = [self.distances[s[i], s[(i+1)%len(s)]]
                          for i in range(0,len(s))]
        return np.sum(pair_distances)
    
    @staticmethod
    def read(stream):
        N = int(stream.readline())
        cities = [np.array([float(x) for x in stream.readline().split()])
                  for _ in range(N)]
        distances = np.array([
            [np.linalg.norm(cities[i]-cities[j]) for j in range(N)]
            for i in range(N)])
        return TSP(distances)
    
    @staticmethod
    def read_matrix(stream):
        distances = []
        for line in stream:
            line = np.array([float(x) for x in line.split()])
            distances.append(line)
        return TSP(np.array(distances))
        
if __name__ == "__main__":
    instance = TSP.read(stdin)
    solution = instance.solve_PSO(n_particles = int(argv[2]),
                                  max_iterations = int(argv[1]),
                                  uncertainty = [0.95, 0.05, 0.05, 0.05])