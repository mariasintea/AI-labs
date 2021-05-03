from random import randint, random


class Ant(object):
    def __init__(self, aco, graph):
        self.__colony = aco
        self.__pheromone = aco.pheromone
        self.__graph = graph
        self.__visited = []  # visited nodes list
        self.__pheromone_delta = []  # the local increase of pheromone
        self.__unvisited = [i for i in range(len(graph))]  # nodes which are allowed for the next selection
        self.__eta = [[0 if i == j else 1 / graph[i][j] for j in range(len(graph))] for i in range(len(graph))]  # heuristic information
        start = randint(0, len(graph) - 1)  # start from any node
        self.__visited.append(start)
        self.__current = start
        self.__visited.remove(start)

    @property
    def visited(self):
        return self.__visited

    @property
    def pheromone_delta(self):
        return self.__pheromone_delta

    def total_cost(self):
        length = 0
        for i in range(0, len(self.__visited)):
            length += self.__graph[self.__visited[i - 1]][self.__visited[i]]
        return length

    def select_next(self):
        denominator = 0
        for i in self.__unvisited:
            denominator += self.__pheromone[self.__current][i] ** self.__colony.alpha * self.__eta[self.__current][i] ** self.__colony.beta

        probabilities = [0 for i in range(len(self.__graph))]  # probabilities for moving to a node in the next step
        for i in range(len(self.__graph)):
            if i in self.__unvisited:  # test if allowed list contains i
                probabilities[i] = self.__pheromone[self.__current][i] ** self.__colony.alpha * self.__eta[self.__current][i] ** self.__colony.beta / denominator

        # select next node by probability roulette
        selected = 0
        rand = random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.__unvisited.remove(selected)
        self.__visited.append(selected)
        self.__current = selected

    # updates pheromone
    def update_pheromone_delta(self):
        self.__pheromone_delta = [[0] * len(self.__graph) for _ in range(len(self.__graph))]
        for k in range(1, len(self.__visited)):
            i = self.__visited[k - 1]
            j = self.__visited[k]
            self.__pheromone_delta[i][j] = self.__colony.Q / self.__graph[i][j]
