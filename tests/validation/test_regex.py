from validation.regex import pattern


def test_regex_for_int():
    assert pattern(r'\d+')('0')
    assert not pattern(r'\d+')('a')


def test_regex_for_single_word():
    assert pattern(r'\w+')('abc')
    assert not pattern(r'\w+')('abc abc')
