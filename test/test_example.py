def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance(3, int)
    assert isinstance("This is a string", str)


def test_boolean():
    validated = True
    assert validated is True
    assert ("hello" == "world") is False


def test_greater_and_less_than():
    assert 3 > 2
    assert 3 < 4


def test_list():
    numbers = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in numbers
    assert False in any_list
    assert 6 not in numbers
