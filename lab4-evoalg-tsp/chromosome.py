from random import randint
import numpy as np


class Chromosome:
    def __init__(self, problem_param=None):
        self.__problemParam = problem_param
        # initialisation of chromosome - random permutation of integers
        self.__representation = list(np.random.permutation(self.__problemParam['size']))
        self.__fitness = 0.0

    @property
    def representation(self):
        return self.__representation

    @property
    def fitness(self):
        return self.__fitness

    @representation.setter
    def representation(self, l=[]):
        self.__representation = l

    @fitness.setter
    def fitness(self, fit=0.0):
        self.__fitness = fit

    # cyclic crossover
    def crossover(self, p2):
        n = len(self.__representation)
        new_representation = [-1] * n
        k = 0
        while new_representation.count(-1) > 0:
            pos = k
            while True:
                new_representation[pos] = self.representation[pos]
                pos = self.representation.index(p2.representation[pos])
                if pos == k:
                    break
            while k < n - 1 and new_representation[k] != -1:
                k += 1
            if k < n - 1:
                pos = k
                while True:
                    new_representation[pos] = p2.representation[pos]
                    pos = p2.representation.index(self.representation[pos])
                    if pos == k:
                        break
            while k < n - 1 and new_representation[k] != -1:
                k += 1

        offspring = Chromosome(self.__problemParam)
        offspring.representation = new_representation
        return offspring

    # swap mutation
    def mutation(self):
        pos_1 = randint(0, len(self.representation) - 1)
        pos_2 = randint(0, len(self.representation) - 1)
        #self.representation[pos_1], self.representation[pos_2] = self.representation[pos_2], self.representation[pos_1]

        if pos_1 > pos_2:
            pos_1, pos_2 = pos_2, pos_1
        self.representation[pos_1:pos_2] = reversed(self.representation[pos_1:pos_2])
