import itertools
import random


# reads data from file
# in: -
# out: n - dimension of read graph, start - starting city, end - ending city
def read_data():
    graph = []
    try:
        f = open("data.in", "r")
    except IOError:
        print("File reading error!")
        return []
    line = f.readline().strip()
    n = int(line)
    for i in range(0, n):
        line = f.readline().strip()
        nrs = line.split(",")
        graph.append(list(map(int, nrs)))
    line = f.readline().strip()
    start = int(line)
    line = f.readline().strip()
    end = int(line)
    f.close()
    return n, start, end, graph


# generates a permutation of cities in given graph
# in: graph - given graph
# out: solution - a permutation of cities in graph
def generate_permutation(graph):
    cities = list(range(len(graph)))
    solution = []
    for i in range(len(graph)):
        random_city = cities[random.randint(0, len(cities) - 1)]
        solution.append(random_city)
        cities.remove(random_city)
    return solution


# calculates the length, including the return to start, of a given route in given graph
# in: graph - given graph, solution - given route
# out: length - the length, including the return to start, of solution in graph
def solution_length_tsp(graph, solution):
    length = 0
    for i in range(0, len(solution)):
        length += graph[solution[i - 1]][solution[i]]
    return length


# calculates the length, without the return to start, of a given route in given graph
# in: graph - given graph, solution - given route
# out: length - the length, without the return to start, of solution in graph
def solution_length_sp(graph, solution):
    length = 0
    for i in range(1, len(solution)):
        length += graph[solution[i - 1]][solution[i]]
    return length


# returns all the permutations starting with the same city of a given route
# in: solution - given route, start - start city, end - end city
# out: permutations - all the permutations starting with the same city of route
def find_all_permutations(solution, start, end):
    permutations = []
    for i in range(1, len(solution)):
        for j in range(i + 1, len(solution)):
            current_permutation = solution.copy()
            current_permutation[i] = solution[j]
            current_permutation[j] = solution[i]
            permutations.append(current_permutation)
    return permutations


# returns all the arrangements starting with the start city and ending with end city of a given route
# in: solution - given route, start - start city, end - end city
# out: all_arrangements - all the arrangements starting with the start city and ending with end city of route
def find_all_arrangements(sol, start, end):
    all_arrangements = []
    solution = sol.copy()
    solution.remove(start)
    solution.remove(end)
    for r in range(len(solution) + 1):
        arrangements_object = itertools.permutations(solution, r)
        arrangements_list = list(arrangements_object)
        for elem in arrangements_list:
            current_arrangement = list(elem)
            current_arrangement.append(end)
            current_arrangement.insert(0, start)
            all_arrangements.append(current_arrangement)
    return all_arrangements


# returns the best permutation and its length from given permutations of starting route, based on the given
#   graph and the given route length computing function
# in: graph - given graph, permutations - given permutations of starting route, solution_length - given
#   route length computing function
# out: best_permutation - the best permutation based on given data, best_length - best_permutation's length
def find_best_permutation(graph, permutations, solution_length):
    best_length = solution_length(graph, permutations[0])
    best_permutation = permutations[0]
    for permutation in permutations:
        current_length = solution_length(graph, permutation)
        if current_length < best_length:
            best_length = current_length
            best_permutation = permutation
    return best_permutation, best_length


# returns the best route and its length based on the given data
# in: graph - given graph, start_solution - given start route, find_all_permutations - given function that
#   calculates all wanted permutations, solution_length - given function that computes the length of a route,
#   start - start city, end - end city
#       find_all_permutations - find_all_permutations for tsp
#                             - find_all_arrangements for shortest path
#       solution_length - solution_length_tsp for tsp
#                       - solution_length_sp for shortest path
# out: current_solution - best route, current_length - current_solution's length
def hill_climbing(graph, start_solution, find_all_permutations, solution_length, start, end):
    current_solution = start_solution
    current_length = solution_length(graph, current_solution)
    permutations = find_all_permutations(current_solution, start, end)
    best_permutation, new_length = find_best_permutation(graph, permutations, solution_length)
    while new_length < current_length:
        current_solution = best_permutation
        current_length = new_length
        permutations = find_all_permutations(current_solution, start, end)
        best_permutation, new_length = find_best_permutation(graph, permutations, solution_length)
    return current_solution, current_length

# writes solution in file
# in: tsp_solution - best route for tsp problem, sp_solution - best route for sp solution
# out: -
def write_solution(tsp_solution, sp_solution):
    f = open("data.out", "w")
    f.write(str(len(tsp_solution[0])) + "\n")
    line = str(tsp_solution[0][0] + 1)
    for i in range(1, len(tsp_solution[0])):
        line = line + ", " + str(tsp_solution[0][i] + 1)
    f.write(line + "\n")
    f.write(str(tsp_solution[1]) + "\n")
    f.write(str(len(sp_solution[0])) + "\n")
    line = str(sp_solution[0][0] + 1)
    for i in range(1, len(sp_solution[0])):
        line = line + ", " + str(sp_solution[0][i] + 1)
    f.write(line + "\n")
    f.write(str(sp_solution[1]) + "\n")


# tests all functions
def tests():
    graph_test = [[0, 1, 2, 4], [1, 0, 3, 15], [2, 3, 0, 6], [4, 15, 6, 0]]
    start_test = 0
    end_test = 2
    perm = generate_permutation(graph_test)
    assert (len(perm) == 4)
    assert (perm.count(0) == 1)
    assert (perm.count(1) == 1)
    assert (perm.count(2) == 1)
    assert (perm.count(3) == 1)

    assert (solution_length_tsp(graph_test, [0, 1, 2, 3]) == 14)
    assert (solution_length_tsp(graph_test, [0, 2, 3, 1]) == 24)
    assert (solution_length_tsp(graph_test, [2, 3, 0, 1]) == 14)
    assert (solution_length_tsp(graph_test, [3, 1, 0, 2]) == 24)

    assert (solution_length_sp(graph_test, [0, 1, 2]) == 4)
    assert (solution_length_sp(graph_test, [2, 1]) == 3)
    assert (solution_length_sp(graph_test, [2, 0, 3]) == 6)
    assert (solution_length_sp(graph_test, [2, 1, 3]) == 18)
    assert (solution_length_sp(graph_test, [2, 1, 3, 0]) == 22)

    assert (find_all_permutations([0, 2, 1, 3], start_test, end_test) == [[0, 1, 2, 3], [0, 3, 1, 2], [0, 2, 3, 1]])
    assert (find_all_permutations([0, 1, 3, 2], start_test, end_test) == [[0, 3, 1, 2], [0, 2, 3, 1], [0, 1, 2, 3]])
    assert (find_all_permutations([1, 2, 3, 0], start_test, end_test) == [[1, 3, 2, 0], [1, 0, 3, 2], [1, 2, 0, 3]])
    assert (find_all_permutations([3, 2, 1, 0], start_test, end_test) == [[3, 1, 2, 0], [3, 0, 1, 2], [3, 2, 0, 1]])

    assert (find_all_arrangements([0, 1, 2], start_test, end_test) == [[0, 2], [0, 1, 2]])
    assert (find_all_arrangements([0, 2], start_test, end_test) == [[0, 2]])
    assert (find_all_arrangements([0, 1, 3, 2], start_test, end_test) == [[0, 2], [0, 1, 2], [0, 3, 2], [0, 1, 3, 2], [0, 3, 1, 2]])
    assert (find_all_arrangements([0, 2, 3, 1], start_test, end_test) == [[0, 2], [0, 3, 2], [0, 1, 2], [0, 3, 1, 2], [0, 1, 3, 2]])

    assert (find_best_permutation(graph_test, [[0, 2], [0, 1, 2], [0, 3, 2], [0, 1, 3, 2], [0, 3, 1, 2]], solution_length_sp) == ([0, 2], 2))
    assert (find_best_permutation(graph_test, [[3, 1, 2, 0], [3, 0, 1, 2], [3, 2, 0, 1]], solution_length_sp) == ([3, 0, 1, 2], 8))
    assert (find_best_permutation(graph_test, [[3, 1, 2, 0], [3, 0, 1, 2], [3, 2, 0, 1]], solution_length_tsp) == ([3, 0, 1, 2], 14))
    assert (find_best_permutation(graph_test, [[0, 1, 2, 3], [0, 3, 1, 2], [0, 2, 3, 1]], solution_length_tsp) == ([0, 1, 2, 3], 14))
    assert (find_best_permutation(graph_test, [[0, 2], [0, 1, 2]], solution_length_sp) == ([0, 2], 2))

    assert (hill_climbing(graph_test, [0, 3, 1, 2], find_all_permutations, solution_length_tsp, start_test, end_test) == ([0, 3, 2, 1], 14))
    assert (hill_climbing(graph_test, [0, 2, 3, 1], find_all_arrangements, solution_length_sp, start_test, end_test) == ([0, 2], 2))

    print("Passed all tests!")


def main():
    tests()
    n, start, end, graph = read_data()
    # for tsp
    perm = generate_permutation(graph)
    perm.remove(0)
    perm.insert(0, 0)
    tsp_solution = hill_climbing(graph, perm, find_all_permutations, solution_length_tsp, 1, 1)
    # for shortest path
    start = start - 1
    end = end - 1
    perm = generate_permutation(graph)
    perm.remove(start)
    perm.insert(0, start)
    perm.remove(end)
    perm.append(end)
    sp_solution = hill_climbing(graph, perm, find_all_arrangements, solution_length_sp, start, end)
    write_solution(tsp_solution, sp_solution)


main()
