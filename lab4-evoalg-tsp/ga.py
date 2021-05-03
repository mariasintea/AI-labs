from random import randint
from chromosome import Chromosome


class GA:
    def __init__(self, param=None, problem_param=None):
        self.__param = param
        self.__problem_param = problem_param
        self.__population = []

    @property
    def population(self):
        return self.__population

    # initialises population
    def initialisation(self):
        for _ in range(0, self.__param['population_size']):
            c = Chromosome(self.__problem_param)
            self.__population.append(c)

    # evaluates fitness of chromosomes in population
    def evaluation(self, graph):
        for c in self.__population:
            c.fitness = self.__problem_param['fitness_function'](c.representation, graph)

    # finds best chromosome in population
    def best_chromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if c.fitness < best.fitness:
                best = c
        return best

    # tournament of k elements
    def selection(self):
        best = randint(0, self.__param['population_size'] - 1)
        for _ in range(self.__param['k'] - 1):
            pos = randint(0, self.__param['population_size'] - 1)
            if self.__population[pos].fitness < self.__population[best].fitness:
                best = pos
        return best

    # puts best chromosome in the new population, generates the rest
    def one_generation_elitism(self, graph):
        new_population = [self.best_chromosome()]
        for _ in range(self.__param['population_size'] - 1):
            parent1 = self.__population[self.selection()]
            parent2 = self.__population[self.selection()]
            offspring = parent1.crossover(parent2)
            offspring.mutation()
            new_population.append(offspring)
        self.__population = new_population
        self.evaluation(graph)
