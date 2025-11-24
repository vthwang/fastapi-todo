import pytest


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


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 2)


def test_person_initialization(default_employee):
    assert default_employee.first_name == "John", "First name should be John"
    assert default_employee.last_name == "Doe", "Last name should be Doe"
    assert default_employee.major == "Computer Science", (
        "Major should be Computer Science"
    )
    assert default_employee.years == 2, "Years should be 2"
