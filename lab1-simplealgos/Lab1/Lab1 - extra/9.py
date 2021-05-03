# returns a matrix containing partial sums of given matrix
# in: n - number of lines, m - number of columns, mat - given matrix of elements
# out: matrix containing partial sums of mat
def partial_sums(n, m, mat):
    matrix = []
    for i in range(0, n):
        line = [0] * m
        line[0] = mat[i][0]
        for j in range(1, m):
            line[j] = line[j - 1] + mat[i][j]
        matrix.append(line)
    return matrix


# returns sum of elements in a rectangle with coordinates between given start point and given end point,
# based on the given partial sum matrix
# in: start - start point coordinates, end - end point coordinates, partials - given partial sum matrix
# out: sum of elements in a rectangle with coordinates between start and end, based on partials
def rectangle_sum(start, end, partials):
    s = 0
    for i in range(start[0], end[0] + 1):
        if start[1] == 0:
            s = s + partials[i][end[1]]
        else:
            s = s + partials[i][end[1]] - partials[i][start[1] - 1]
    return s


# tests rectangle_sum function
# in : -
# out : -
def test_rectangle_sum():
    mat = [[0, 2, 5, 4, 1], [4, 8, 2, 3, 7], [6, 3, 4, 6, 2], [7, 3, 1, 8, 3], [1, 5, 7, 9, 4]]
    partials = partial_sums(5, 5, mat)
    assert (rectangle_sum([1, 1], [3, 3], partials) == 38)
    assert (rectangle_sum([2, 2], [4, 4], partials) == 44)
    assert (rectangle_sum([2, 2], [2, 2], partials) == 4)
    assert (rectangle_sum([0, 0], [1, 1], partials) == 14)
    assert (rectangle_sum([0, 0], [4, 4], partials) == 105)


test_rectangle_sum()
