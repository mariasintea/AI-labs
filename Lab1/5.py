# returns the element that appears more than once in given array
# in: n - number of elements in array, elems - given array of elements
# out: element that appears more than once in elems
def apparitions(n, elems):
    fr = [0] * n
    for elem in elems:
        if fr[elem] == 1:
            return elem
        else:
            fr[elem] = fr[elem] + 1


# tests apparitions function
# in : -
# out : -
def test_apparitions():
    assert(apparitions(5, [1, 2, 3, 4, 2]) == 2)
    assert(apparitions(6, [1, 4, 3, 4, 2, 5]) == 4)
    assert(apparitions(3, [1, 1, 2]) == 1)
    assert(apparitions(7, [1, 4, 3, 5, 2, 6, 3]) == 3)


test_apparitions()
