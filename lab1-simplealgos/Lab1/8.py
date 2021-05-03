from queue import Queue


# generates binary form of numbers between 1 and given number
# in: n - given number
# out: array containing binary form of numbers between 1 and n
def binary_numbers(n):
    q = Queue()
    q.put(1)
    result = [1]
    nr = 1
    while nr < n:
        current = q.get()
        q.put(current * 10)
        result.append(current * 10)
        nr = nr + 1
        if nr < n:
            q.put(current * 10 + 1)
            result.append(current * 10 + 1)
            nr = nr + 1
    return result


# tests binary_numbers function
# in : -
# out : -
def test_binary_numbers():
    assert (binary_numbers(4) == [1, 10, 11, 100])
    assert (binary_numbers(10) == [1, 10, 11, 100, 101, 110, 111, 1000, 1001, 1010])
    assert (binary_numbers(13) == [1, 10, 11, 100, 101, 110, 111, 1000, 1001, 1010, 1011, 1100, 1101])
    assert (binary_numbers(16) == [1, 10, 11, 100, 101, 110, 111, 1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111, 10000])


test_binary_numbers()