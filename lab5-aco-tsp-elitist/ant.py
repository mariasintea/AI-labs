from random import randint, uniform, sample


class Edge:
    def __init__(self, a, b, cost, initial_pheromone):
        self.a = a
        self.b = b
        self.__cost = cost
        self.__pheromone = initial_pheromone

    @property
    def pheromone(self):
        return self.__pheromone

    @pheromone.setter
    def pheromone(self, val=0):
        self.__pheromone = val

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, val=0):
        self.__cost = val


class Ant(object):
    def __init__(self, params, n, edges):
        self.__params = params
        self.__visited = []  # nodes visited during ant's tour
        self.__n = n  # number of vertices
        self.__edges = edges

    # calculates the length of the ant's current tour
    def total_cost(self):
        length = 0
        for i in range(0, self.__n):
            length += self.__edges[self.__visited[i - 1]][self.__visited[i]].cost
        return length

    # finds a new tour
    def find_tour(self):
        self.__visited = [randint(0, self.__n - 1)]
        while len(self.__visited) < self.__n:
            self.__visited.append(self._select_next())
        return self.__visited

    # selects next vertex to be added in ant's current tour
    def _select_next(self):
        unvisited = [node for node in range(self.__n) if node not in self.__visited]
        exploration = uniform(0.0, 1.0)
        if exploration < 0.10:
            # select closest city
            min = float("inf")
            for unvisited_node in unvisited:
                if self.__edges[self.__visited[-1]][unvisited_node].cost < min:
                    min = self.__edges[self.__visited[-1]][unvisited_node].cost
                    min_node = unvisited_node
            explored_node = min_node
            return explored_node
        else:
            # select city based on probability
            sum = 0.0
            for unvisited_node in unvisited:
                sum += (self.__edges[self.__visited[-1]][unvisited_node].pheromone ** self.__params["alpha"]) * (1.0 / self.__edges[self.__visited[-1]][unvisited_node].cost) ** self.__params["beta"]
            random_value = uniform(0.0, 1.0)
            probability = 0.0
            for unvisited_node in sample(unvisited, len(unvisited)):
                probability += ((self.__edges[self.__visited[-1]][unvisited_node].pheromone ** self.__params["alpha"]) * (1.0 / self.__edges[self.__visited[-1]][unvisited_node].cost ** self.__params["beta"])) / sum
                if probability >= random_value:
                    return unvisited_node

    def update_edges(self, edges):
        self.__edges = edges
