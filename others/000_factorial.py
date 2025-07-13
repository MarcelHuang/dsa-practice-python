import pytest


def factorial(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Factorial expects an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def test_factorial_of_zero():
    assert factorial(0) == 1


def test_factorial_of_one():
    assert factorial(1) == 1


def test_factorial_of_positive_number():
    assert factorial(3) == 6


def test_factorial_larger_number():
    assert factorial(5) == 120


def test_factorial_negative_number():
    with pytest.raises(ValueError):
        factorial(-1)


def test_factorial_with_string():
    with pytest.raises(TypeError):
        factorial("hello")


def test_factorial_with_float():
    with pytest.raises(TypeError):
        factorial(3.14)
