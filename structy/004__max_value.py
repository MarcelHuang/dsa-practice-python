from hypothesis import given, strategies as st


def max_value(nums):
    largest = float("-inf")
    for num in nums:
        if num > largest:
            largest = num
    return largest


def test_max_value_basic():
    """Test with a simple list of positive numbers"""
    assert max_value([1, 3, 2, 5, 4]) == 5


def test_max_value_negative_numbers():
    """Test with negative numbers"""
    assert max_value([-10, -5, -3, -8]) == -3


def test_max_value_mixed_numbers():
    """Test with mix of positive and negative"""
    assert max_value([-5, 3, -1, 8, 2]) == 8


def test_max_value_single_element():
    """Test with single element"""
    assert max_value([42]) == 42


def test_max_value_duplicates():
    """Test with duplicate maximum values"""
    assert max_value([5, 5, 3, 5, 1]) == 5


def test_max_value_with_zero():
    """Test including zero"""
    assert max_value([0, -5, -10]) == 0
    assert max_value([0, 5, 10]) == 10


def test_max_value_floats():
    """Test with floating point numbers"""
    assert max_value([1.5, 2.7, 1.2, 3.8]) == 3.8


def test_max_value_large_numbers():
    """Test with very large numbers"""
    assert max_value([1000000, 999999, 1000001]) == 1000001


def test_max_value_empty_list():
    """Test edge case: empty list"""
    # This will actually return float('-inf') with current implementation
    # You might want to handle this case differently
    assert max_value([]) == float("-inf")


def test_max_value_with_infinity():
    """Test with infinity values"""
    assert max_value([1, float("inf"), 5]) == float("inf")
    assert max_value([float("-inf"), -5, -1]) == -1


# Property-based testing (if you have hypothesis installed)
@given(st.lists(st.integers(), min_size=1))
def test_max_value_property_based(nums):
    """Property: result should equal Python's built-in max()"""
    assert max_value(nums) == max(nums)


@given(st.lists(st.integers(), min_size=1))
def test_max_value_equals_builtin_max(nums):
    """Property: Our function should behave like Python's built-in max()"""
    assert max_value(nums) == max(nums)


@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_max_value_with_floats(nums):
    """Test with generated float values"""
    result = max_value(nums)
    assert result == max(nums)
    assert result in nums  # Maximum should be one of the input values


@given(st.lists(st.integers(), min_size=1))
def test_max_value_properties(nums):
    """Test mathematical properties of maximum"""
    result = max_value(nums)

    # Property 1: Result should be in the original list
    assert result in nums

    # Property 2: Result should be >= all elements
    assert all(result >= num for num in nums)

    # Property 3: There should be at least one element equal to result
    assert any(result == num for num in nums)


@given(st.lists(st.integers(), min_size=1), st.integers())
def test_max_value_with_added_element(nums, new_element):
    """Property: Adding element changes max predictably"""
    original_max = max_value(nums)
    extended_nums = nums + [new_element]
    new_max = max_value(extended_nums)

    # New max should be either the original max or the new element
    assert new_max == max(original_max, new_element)


@given(st.lists(st.integers(), min_size=2))
def test_max_value_invariant_under_permutation(nums):
    """Property: Order shouldn't matter"""
    import random

    shuffled = nums.copy()
    random.shuffle(shuffled)

    assert max_value(nums) == max_value(shuffled)


@given(st.lists(st.integers(min_value=-1000, max_value=1000), min_size=1, max_size=10))
def test_max_value_bounded_inputs(nums):
    """Test with bounded integer ranges"""
    result = max_value(nums)
    assert -1000 <= result <= 1000
    assert result in nums


@given(st.lists(st.just(42), min_size=1, max_size=5))
def test_max_value_all_same_elements(nums):
    """Property: If all elements are the same, max equals that element"""
    assert max_value(nums) == 42


# Test with different numeric types
@given(st.lists(st.one_of(st.integers(), st.floats(allow_nan=False)), min_size=1))
def test_max_value_mixed_numeric_types(nums):
    """Test with mixed integers and floats"""
    result = max_value(nums)
    assert result == max(nums)


# Create custom strategies for specific test scenarios
negative_numbers = st.lists(st.integers(max_value=-1), min_size=1)
positive_numbers = st.lists(st.integers(min_value=1), min_size=1)


@given(negative_numbers)
def test_max_value_all_negative(nums):
    """Property: Max of negative numbers should be negative"""
    result = max_value(nums)
    assert result < 0
    assert result in nums


@given(positive_numbers)
def test_max_value_all_positive(nums):
    """Property: Max of positive numbers should be positive"""
    result = max_value(nums)
    assert result > 0
    assert result in nums


@given(st.lists(st.nothing(), min_size=0, max_size=0))
def test_max_value_empty_list_behavior(nums):
    """Test behavior with empty lists"""
    # Your current implementation returns float('-inf')
    # You might want to test if this is the desired behavior
    result = max_value(nums)
    assert result == float("-inf")

    # Or if you modify to raise an exception:
    # with pytest.raises(ValueError):
    #     max_value(nums)
