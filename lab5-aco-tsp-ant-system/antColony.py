from ant import Ant


class AntColony:
    def __init__(self, params):
        self.__params = params

    @property
    def alpha(self):
        return self.__params["alpha"]

    @property
    def beta(self):
        return self.__params["beta"]

    @property
    def Q(self):
        return self.__params["Q"]

    @property
    def pheromone(self):
        return self.__pheromone

    def createPheromoneMatrix(self, graph):
        n = len(graph)
        self.__pheromone = [[1 / (n * n)] * n for _ in range(n)]

    def updatePheromone(self, ants):
        for i, row in enumerate(self.__pheromone):
            for j, col in enumerate(row):
                self.__pheromone[i][j] *= self.__params["rho"]
                for ant in ants:
                    self.__pheromone[i][j] += ant.pheromone_delta[i][j]

    def solve(self, graph):
        best_cost = float('inf')
        best_solution = []
        for gen in range(self.__params["generations"]):
            # initialize colony
            ants = [Ant(self, graph) for _ in range(self.__params["ant_count"])]

            for ant in ants:
                for _ in range(len(graph) - 1):
                    ant.select_next()
                cost = ant.total_cost()
                if cost < best_cost:
                    best_cost = cost
                    best_solution = list(ant.visited)
                # update pheromone for ant
                ant.update_pheromone_delta()

            self.updatePheromone(ants)
            # print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
            print(best_cost)

        return best_solution, best_cost
