from ga import GA


# reads data from file
# in: -
# out: adjacency - adjacency matrix of graph, degrees - degrees of nodes in graph,
#      neighbors - lists of neighbours for each node and graph number of edges
def read_graph():
    graph = []
    try:
        f = open("data.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    line = f.readline().strip()
    n = int(line)
    for _ in range(0, n):
        line = f.readline().strip()
        nrs = line.split(",")
        graph.append(list(map(int, nrs)))
    f.close()
    return graph


# function that helps to evaluate the quality of previous communities inside a network
# in: chromosome - given chromosome, adjacency - adjacency matrix of graph, degrees - degrees of nodes in graph,
#     no_edges - graph number of edges
# out: modularity result
def solution_length(chromosome, graph):
    length = 0
    for i in range(0, len(chromosome)):
        length += graph[chromosome[i - 1]][chromosome[i]]
    return length


# writes solution
# in: solution - problem solution, fitness_evolution - fitnesses obtained along computation process,
#     communities_number_evolution - communities numbers obtained along computation process
# out: -
def write_solution(solution, graph):
    print("Solution length:", solution_length(solution, graph))
    print("Solution:", solution)


# main function
def main():
    # initialisation
    graph = read_graph()
    generations_count = 300
    population_size = 100
    parameters = {
        'k': 15,  # tournament dimension
        'population_size': population_size,
        'fitness_function': solution_length
    }
    parameters_2 = {
        'size': len(graph),
        'population_size': population_size,
        'fitness_function': solution_length
    }
    ga = GA(parameters, parameters_2)

    ga.initialisation()
    ga.evaluation(graph)
    for _ in range(generations_count):
        ga.one_generation_elitism(graph)
        best_chromosome = ga.best_chromosome()
        print(best_chromosome.fitness)

    solution = ga.best_chromosome()
    write_solution(solution.representation, graph)


if __name__ == '__main__':
    main()
