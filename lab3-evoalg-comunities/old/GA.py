from random import randint

from old.Chromosome import Chromosome


class GA:
    def __init__(self, param=None, problem_param=None):
        self.__param = param
        self.__problem_param = problem_param
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialisation(self):
        for _ in range(0, self.__param['population_size']):
            c = Chromosome(self.__problem_param)
            self.__population.append(c)

    def evaluation(self, adjacency, degrees, no_edges):
        for c in self.__population:
            c.fitness = self.__problem_param['fitness_function'](c.representation, adjacency, degrees, no_edges)

    def best_chromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if c.fitness > best.fitness:
                best = c
        return best

    def worst_chromosome(self):
        worst = self.__population[0]
        for c in self.__population:
            if c.fitness > worst.fitness:
                worst = c
        return worst

    def selection(self):
        pos1 = randint(0, self.__param['population_size'] - 1)
        pos2 = randint(0, self.__param['population_size'] - 1)
        if self.__population[pos1].fitness > self.__population[pos2].fitness:
            return pos1
        else:
            return pos2

    def one_generation(self, adjacency, degrees, no_edges):
        new_pop = []
        for _ in range(self.__param['population_size']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            new_pop.append(off)
        self.__population = new_pop
        self.evaluation(adjacency, degrees, no_edges)

    def one_generation_elitism(self, adjacency, degrees, no_edges):
        new_pop = [self.best_chromosome()]
        for _ in range(self.__param['population_size'] - 1):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            new_pop.append(off)
        self.__population = new_pop
        self.evaluation(adjacency, degrees, no_edges)

    def one_generation_steady_state(self):
        for _ in range(self.__param['population_size']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            off.fitness = self.__problem_param['fitness_function'](off.repres)
            worst = self.worst_chromosome()
            if off.fitness < worst.fitness:
                worst = off
