# returns the k-th biggest element in given array
# in: n - number of elements in array, elems - given array of elements, k - given index
# out: the k-th biggest element in numbers
def max_k(n, numbers, k):
    numbers.sort()
    return numbers[n - k]


# tests max_k function
# in : -
# out : -
def test_max_k():
    assert (max_k(6, [7, 4, 6, 3, 9, 1], 2) == 7)
    assert (max_k(6, [7, 4, 6, 3, 9, 1], 1) == 9)
    assert (max_k(6, [7, 4, 6, 3, 9, 1], 6) == 1)
    assert (max_k(6, [7, 4, 6, 3, 9, 1], 4) == 4)


test_max_k()
