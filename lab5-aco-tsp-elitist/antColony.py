from random import uniform, randint, choice

from ant import Ant, Edge


class AntColony:
    def __init__(self, params, graph):
        self.__params = params
        self.__n = len(graph)
        # initialize edges with correspondent weight and initial pheromone
        self.__edges = [[None] * len(graph) for _ in range(len(graph))]
        for i in range(len(graph)):
            for j in range(i + 1, len(graph)):
                self.__edges[i][j] = self.__edges[j][i] = Edge(i, j, graph[i][j], self.__params["Q"])

    def _update_pheromone(self, tour, distance, rho=1.0):
        for i in range(self.__n):
            self.__edges[tour[i - 1]][tour[i]].pheromone += rho * 1 / distance

    # calculates best cost and best tour
    def solve(self):
        best_cost = float('inf')
        best_solution = []
        # initialize colony
        ants = [Ant(self.__params, self.__n, self.__edges) for _ in range(self.__params["colony_size"])]

        for gen in range(self.__params["generations"]):
            for ant in ants:
                current_tour = ant.find_tour()
                current_cost = ant.total_cost()
                self._update_pheromone(current_tour, current_cost)
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_solution = current_tour

            # update pheromone
            for i in range(self.__n):
                for j in range(i + 1, self.__n):
                    self.__edges[i][j].pheromone *= (1.0 - self.__params["rho"])
            self._update_pheromone(best_solution, best_cost, self.__params["rho"])
            print(best_cost)

            """# for dynamic graph
            r = uniform(0, 1)
            if r < 0.5 == 0:
                self._modify(ants)"""

        return best_solution, best_cost

    def _modify(self, ants):
        node1 = randint(0, self.__n - 1)
        node2 = choice([i for i in range(0, self.__n) if i != node1])
        deviation = uniform(-100, 100)
        self.__edges[node1][node2].cost = self.__edges[node2][node1].cost = self.__edges[node1][node2].cost + deviation

        for ant in ants:
            ant.update_edges(self.__edges)
