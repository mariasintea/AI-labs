from math import sqrt

from antColony import AntColony


def readData():
    try:
        f = open("static_graph.txt", "r")
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


def distance(city1, city2):
    return sqrt((city1["x"] - city2["x"]) * (city1["x"] - city2["x"]) + (city1["y"] - city2["y"]) * (city1["y"] - city2["y"]))


def createDistanceMatrix(cities):
    n = len(cities)
    mat = [[0] * n for _ in range(n)]
    for i in range(0, n):
        for j in range(i+1, n):
            mat[i][j] = mat[j][i] = distance(cities[i], cities[j])
    return mat


def main():
    cities = readData()
    distanceMatrix = createDistanceMatrix(cities)
    params = {
        "ant_count": 10,
        "generations": 300,
        "alpha": 1.0,
        "beta": 10.0,
        "rho": 0.5,  # evaporation rate
        "Q": 10  # constant
    }
    aco = AntColony(params)
    aco.createPheromoneMatrix(distanceMatrix)
    path, cost = aco.solve(distanceMatrix)
    print('cost: {}, path: {}'.format(cost, path))


if __name__ == '__main__':
    main()
