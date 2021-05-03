from random import randint, uniform


class Chromosome:
    def __init__(self, problem_param=None):
        self.__problemParam = problem_param
        # initialisation of chromosome - random integers
        self.__representation = [randint(0, problem_param['population_size'] - 1) for _ in range(problem_param['size'])]
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

    # n-point crossover
    def crossover(self, p2):
        new_representation = []
        # generate n random different positions
        positions = [0]
        length = len(self.__representation)
        for _ in range(self.__problemParam['n']):
            current_pos = randint(1, length - 1)
            while current_pos in positions:
                current_pos = randint(1, length - 1)
            positions.append(current_pos)
        positions.append(length)
        positions.sort()

        for i in range(len(positions) - 1):
            for pos in range(positions[i], positions[i + 1]):
                if i % 2 == 0:
                    new_representation.append(self.__representation[pos])
                else:
                    new_representation.append(p2.representation[pos])

        offspring = Chromosome(self.__problemParam)
        offspring.representation = new_representation
        return offspring

    # creep mutation
    def mutation(self):
        for i in range(0, len(self.representation)):
            r = uniform(0, 1)
            if r < self.__problemParam['pm']:
                to_add = 1
                if r < self.__problemParam['pm']/2 or self.__representation[i] == self.__problemParam['size']:
                    to_add = -1
                self.__representation[i] += to_add
