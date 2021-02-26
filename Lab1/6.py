# returns the majority element in given array
# in: n - number of elements in array, elems - given array of elements
# out: majority element in elems
def element(n, elems):
    fr = [0] * n
    for elem in elems:
        if fr[elem] + 1 > n/2:
            return elem
        else:
            fr[elem] = fr[elem] + 1
    print(n/2)
    return -1


# tests element function
# in : -
# out : -
def test_element():
    assert(element(11, [2, 8, 7, 2, 2, 5, 2, 3, 1, 2, 2]) == 2)
    assert(element(6, [1, 4, 4, 4, 2, 4]) == 4)
    assert(element(3, [1, 1, 2]) == 1)
    assert(element(7, [3, 4, 3, 5, 2, 3, 3]) == 3)


test_element()
