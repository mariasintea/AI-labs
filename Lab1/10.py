# returns number of ones at the end of given array
# in: j - current index, array - given array
# out: number of ones at the end of array
def number_of_ones(j, array):
    if array[j] == 0 or j == 0:
        return 0
    return number_of_ones(j - 1, array) + 1


# returns index of line containing most ones in a given matrix
# in: n - number of lines, m - number of columns
#     mat - given matrix
# out: index of line containing most ones in mat
def most_ones(n, m, mat):
    maxim = 0
    index = -1
    for i in range(0, n):
        nr_ones = number_of_ones(m - 1, mat[i])
        if nr_ones > maxim:
            maxim = nr_ones
            index = i
    return index


# tests most_ones function
# in : -
# out : -
def test_most_ones():
    assert(most_ones(3, 5, [[0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1]]) == 1)
    assert(most_ones(3, 5, [[1, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1]]) == 0)
    assert(most_ones(2, 5, [[0, 0, 0, 1, 1], [0, 0, 1, 1, 1]]) == 1)
    assert(most_ones(2, 5, [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]) == -1)


test_most_ones()
