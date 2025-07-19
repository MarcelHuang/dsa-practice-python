from hypothesis import given, strategies as st


@given(st.integers())
def test_is_integer(n):
    print(f"called with {n}")
    assert isinstance(n, int)


def selection_sort(lst):
    result = []
    while lst:
        smallest = min(lst)
        result.append(smallest)
        lst.remove(smallest)
    return result


@given(st.lists(st.integers() | st.floats(allow_nan=False)))
def test_sort_correct(lst):
    print(f"called with {lst}")
    assert selection_sort(lst.copy()) == sorted(lst)


test_is_integer()
test_sort_correct()
