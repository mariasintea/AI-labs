from math import sqrt


# returns the euclidean distance between the given points
# in: a - tuple of two elements, first given point,
#     b - tuple of two elements, second given point
# out: euclidean distance between a and b
def distance(a, b):
    return sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


# tests distance function
# in : -
# out : -
def test_distance():
    assert(distance((1, 5), (4, 1)) == 5.0)
    assert(distance((1, 2), (1, 2)) == 0.0)
    assert(distance((1, 5), (1, 4)) == 1.0)
    assert(distance((0, 0), (4, 3)) == 5.0)


test_distance()
