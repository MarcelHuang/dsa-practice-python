def greet(s: str) -> str:
    return "hey " + s


def test_00():
    assert greet("alvin") == "hey alvin"


def test_01():
    assert greet("jason") == "hey jason"


def test_02():
    assert greet("how now brown cow") == "hey how now brown cow"
