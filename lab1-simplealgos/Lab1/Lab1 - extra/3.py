# returns the scalar product of two given arrays
# in: n - number of elements in arrays, a, b - given array of elements
# out: the scalar product of a and b
def product(n, a, b):
    sol = 0
    for i in range(0, n):
        sol = sol + a[i] * b[i]
    return sol


# tests product function
# in : -
# out : -
def test_product():
    assert (product(5, [1, 0, 2, 0, 3], [1, 2, 0, 3, 1]) == 4)
    assert (product(5, [1, 0, 2, 0, 0], [1, 2, 0, 3, 1]) == 1)
    assert (product(5, [0, 0, 2, 0, 3], [1, 2, 0, 3, 1]) == 3)
    assert (product(5, [1, 0, 2, 0, 3], [1, 0, 1, 3, 1]) == 6)
    assert (product(5, [1, 0, 2, 0, 3], [0, 0, 0, 0, 0]) == 0)


test_product()
