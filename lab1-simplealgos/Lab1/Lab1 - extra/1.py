# returns the last word in given string, ordered alphabetically
# in: text - given string
# out: the last word in text, ordered alphabetically
def last_word(text):
    words = text.split(' ')
    words.sort()
    return words[len(words) - 1]


# tests last_word function
# in : -
# out : -
def test_last_word():
    assert (last_word("Ana are mere rosii si galbene") == "si")
    assert (last_word("Ana zice ca are mere rosii si galbene") == "zice")
    assert (last_word("Ana are mere") == "mere")
    assert (last_word("Ana are") == "are")


test_last_word()
