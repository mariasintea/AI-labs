from math import sqrt

from antColony import AntColony


# read graph from file
def read_data():
    try:
        f = open("graph.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    f.readline()
    f.readline()
    f.readline()
    n = int(f.readline().strip().split()[1])
    f.readline()
    f.readline()
    cities = []
    for _ in range(n):
        ind, x, y = f.readline().strip().split()
        cities.append({"index": int(ind), "x": float(x), "y": float(y)})
    f.close()
    return cities


# calculates geometric distance between two cities
def distance(city1, city2):
    return sqrt((city1["x"] - city2["x"]) * (city1["x"] - city2["x"]) + (city1["y"] - city2["y"]) * (city1["y"] - city2["y"]))


# creates distance matrix based on cities coordinates
def create_distance_matrix(cities):
    n = len(cities)
    mat = [[0] * n for _ in range(n)]
    for i in range(0, n):
        for j in range(i+1, n):
            mat[i][j] = mat[j][i] = distance(cities[i], cities[j])
    return mat


def main():
    cities = read_data()
    distance_matrix = create_distance_matrix(cities)
    params = {
        "colony_size": 20,
        "generations": 300,
        "alpha": 1.0,  # importance of trace
        "beta": 3.0,  # importance of visibility
        "rho": 0.1,  # evaporation rate
        "Q": 1.0  # quantity of pheromone left by an ant
    }
    aco = AntColony(params, distance_matrix)
    path, cost = aco.solve()
    print('cost: {}, path: {}'.format(cost, path))


if __name__ == '__main__':
    main()
