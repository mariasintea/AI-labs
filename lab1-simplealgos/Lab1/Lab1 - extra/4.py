# returns the words that appear only once in given string
# in: text - given string
# out: the words that appear only once in text
def once_words(text):
    words = text.split(' ')
    solution = []
    for word in words:
        if words.count(word) == 1:
            solution.append(word)
    return solution


# tests once_words function
# in : -
# out : -
def test_once_words():
    assert (once_words("ana are ana are mere rosii ana") == ['mere', 'rosii'])
    assert (once_words("ana are mere si ana are pere") == ['mere', 'si', 'pere'])
    assert (once_words("ana are ana are") == [])
    assert (once_words("ana are mere") == ['ana', 'are', 'mere'])


test_once_words()
