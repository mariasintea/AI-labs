import networkx as nx
from ga import GA


# reads data from file
# in: -
# out: adjacency - adjacency matrix of graph, degrees - degrees of nodes in graph,
#      neighbors - lists of neighbours for each node and graph number of edges
def read_graph():
    graph = nx.read_gml("krebs.gml", label="id")
    adjacency = [[0] * (len(graph) + 1) for _ in range(len(graph) + 1)]
    degrees = [0]
    neighbors = [[]]
    for i in graph.adj:
        current_neighbours = []
        for j in graph.adj[i]:
            current_neighbours.append(j)
            adjacency[i][j] = adjacency[j][i] = 1
        neighbors.append(current_neighbours)
        degrees.append(len(current_neighbours))
    return adjacency, degrees, neighbors, len(graph.edges)


# function that helps to evaluate the quality of previous communities inside a network
# in: chromosome - given chromosome, adjacency - adjacency matrix of graph, degrees - degrees of nodes in graph,
#     no_edges - graph number of edges
# out: modularity result
def modularity(chromosome, adjacency, degrees, no_edges):
    M = 2 * no_edges
    Q = 0.0
    for i in range(0, len(adjacency)):
        for j in range(0, len(adjacency)):
            if chromosome[i] == chromosome[j]:
                Q += (adjacency[i][j] - degrees[i] * degrees[j] / M)
    return Q * 1 / M


# writes solution
# in: solution - problem solution, fitness_evolution - fitnesses obtained along computation process,
#     communities_number_evolution - communities numbers obtained along computation process
# out: -
def write_solution(solution, fitness_evolution, communities_number_evolution):
    unique_communities = []
    comunity_label = {}
    for i in solution.representation:
        if i not in unique_communities:
            unique_communities.append(i)
            comunity_label[i] = len(comunity_label) + 1
    print("communities count: " + str(len(unique_communities)))
    for i in range(0, len(solution.representation)):
        print("node " + str(i + 1) + " belongs to community " + str(comunity_label[solution.representation[i]]))
    #print("the fitness evolution is :" + str(fitness_evolution))
    #print("the communities count evolution is :" + str(communities_number_evolution))


# main function
def main():
    # initialisation
    adjacency, degrees, neighbors, no_edges = read_graph()
    generations_count = 100
    population_size = 100
    parameters = {
        'k': 20,  # tournament dimension
        'population_size': population_size,
        'fitness_function': modularity
    }
    parameters_2 = {
        'pm': 0.1,  # mutation rate
        'n': 3,  # number of cuts at crossover
        'size': len(adjacency),
        'population_size': population_size,
        'fitness_function': modularity
    }
    ga = GA(parameters, parameters_2)
    fitness_evolution = []
    communities_number_evolution = []

    ga.initialisation()
    ga.evaluation(adjacency, degrees, no_edges)
    for g in range(generations_count):
        ga.one_generation_elitism(adjacency, degrees, no_edges)
        best_chromosome = ga.best_chromosome()
        fitness_evolution.append('{:.3}'.format(best_chromosome.fitness))
        unique_communities = []
        for i in best_chromosome.representation:
            if i not in unique_communities:
                unique_communities.append(i)
        communities_number_evolution.append(len(unique_communities))
        print(best_chromosome.fitness)

    solution = ga.best_chromosome()
    write_solution(solution, fitness_evolution, communities_number_evolution)


if __name__ == '__main__':
    main()
