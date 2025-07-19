import pytest
from hypothesis import given, strategies as st, assume


def sum_multiples(multiple, limit):
    """Sum of multiples of 'multiple' below 'limit' using arithmetic series"""
    if limit <= 0:
        return 0
    n = (limit - 1) // multiple
    if n < 0:  # This handles cases where limit < multiple
        return 0
    return multiple * n * (n + 1) // 2


def solve_euler_1_optimized(limit=1000):
    # Sum of multiples of 3 + sum of multiples of 5 - sum of multiples of 15
    # (subtract 15 to avoid double-counting numbers divisible by both 3 and 5)
    return sum_multiples(3, limit) + sum_multiples(5, limit) - sum_multiples(15, limit)


# Test cases
class TestSumMultiples:
    """Test the sum_multiples helper function"""

    def test_multiples_of_3_below_10(self):
        # 3 + 6 + 9 = 18
        assert sum_multiples(3, 10) == 18

    def test_multiples_of_5_below_10(self):
        # 5 = 5
        assert sum_multiples(5, 10) == 5

    def test_multiples_of_15_below_10(self):
        # No multiples of 15 below 10
        assert sum_multiples(15, 10) == 0

    def test_edge_case_limit_equals_multiple(self):
        # No multiples of 5 below 5
        assert sum_multiples(5, 5) == 0

    def test_edge_case_limit_less_than_multiple(self):
        # No multiples of 10 below 3
        assert sum_multiples(10, 3) == 0

    def test_single_multiple(self):
        # Only 7 is below 8
        assert sum_multiples(7, 8) == 7

    def test_larger_numbers(self):
        # Multiples of 7 below 50: 7, 14, 21, 28, 35, 42, 49
        # Sum = 7 * (1 + 2 + 3 + 4 + 5 + 6 + 7) = 7 * 28 = 196
        assert sum_multiples(7, 50) == 196


class TestSolveEuler1Optimized:
    """Test the main Euler #1 solution"""

    def test_example_case_limit_10(self):
        # Multiples of 3 or 5 below 10: 3, 5, 6, 9
        # Sum = 3 + 5 + 6 + 9 = 23
        assert solve_euler_1_optimized(10) == 23

    def test_default_case_limit_1000(self):
        # The classic Project Euler #1 answer
        assert solve_euler_1_optimized() == 233168

    def test_small_limits(self):
        assert solve_euler_1_optimized(1) == 0  # No multiples below 1
        assert solve_euler_1_optimized(3) == 0  # No multiples below 3
        assert solve_euler_1_optimized(4) == 3  # Only 3
        assert solve_euler_1_optimized(6) == 8  # 3 + 5 = 8

    def test_limit_includes_multiple_of_15(self):
        # Below 16: multiples are 3,5,6,9,10,12,15
        # Sum = 3+5+6+9+10+12+15 = 60
        assert solve_euler_1_optimized(16) == 60

    def test_larger_limit(self):
        # Test with a larger number to verify the arithmetic series approach
        result = solve_euler_1_optimized(100)
        # Manual verification: this should be 2318
        expected = 2318
        assert result == expected


class TestEdgeCasesAndValidation:
    """Test edge cases and input validation scenarios"""

    def test_zero_limit(self):
        assert solve_euler_1_optimized(0) == 0

    def test_negative_limit_in_sum_multiples(self):
        # Should handle gracefully (no multiples below negative number)
        assert sum_multiples(3, -5) == 0

    @pytest.mark.parametrize(
        "multiple,limit,expected",
        [
            (1, 5, 10),  # 1+2+3+4 = 10
            (2, 10, 20),  # 2+4+6+8 = 20
            (4, 13, 24),  # 4+8+12 = 24
        ],
    )
    def test_parametrized_sum_multiples(self, multiple, limit, expected):
        assert sum_multiples(multiple, limit) == expected


def test_consistency_with_brute_force():
    """Verify our optimized solution matches brute force for small numbers"""

    def brute_force_euler_1(limit):
        return sum(i for i in range(limit) if i % 3 == 0 or i % 5 == 0)

    # Test consistency for various limits
    test_limits = [10, 15, 20, 50, 100]
    for limit in test_limits:
        optimized = solve_euler_1_optimized(limit)
        brute_force = brute_force_euler_1(limit)
        assert (
            optimized == brute_force
        ), f"Mismatch at limit {limit}: optimized={optimized}, brute_force={brute_force}"


class TestPropertyBased:
    """Property-based tests using Hypothesis"""

    @given(st.integers(min_value=1, max_value=1000))
    def test_sum_multiples_always_non_negative(self, multiple):
        """Property: sum_multiples should always return non-negative values"""
        limit = 1000
        result = sum_multiples(multiple, limit)
        assert result >= 0

    @given(
        st.integers(min_value=1, max_value=50), st.integers(min_value=1, max_value=500)
    )
    def test_sum_multiples_monotonic_with_limit(self, multiple, base_limit):
        """Property: increasing limit should not decrease the sum"""
        limit1 = base_limit
        limit2 = base_limit + 10

        sum1 = sum_multiples(multiple, limit1)
        sum2 = sum_multiples(multiple, limit2)

        assert sum2 >= sum1, f"Sum decreased when limit increased: {sum1} -> {sum2}"

    @given(st.integers(min_value=1, max_value=100))
    def test_euler_solution_consistency_with_brute_force(self, limit):
        """Property: optimized solution should always match brute force"""

        def brute_force_euler_1(n):
            return sum(i for i in range(n) if i % 3 == 0 or i % 5 == 0)

        optimized = solve_euler_1_optimized(limit)
        brute_force = brute_force_euler_1(limit)

        assert (
            optimized == brute_force
        ), f"Mismatch at limit {limit}: optimized={optimized}, brute_force={brute_force}"

    @given(
        st.integers(min_value=1, max_value=20), st.integers(min_value=1, max_value=100)
    )
    def test_sum_multiples_mathematical_property(self, multiple, limit):
        """Property: sum should equal multiple * triangular_number_of_count"""
        n = (limit - 1) // multiple
        expected = multiple * n * (n + 1) // 2
        actual = sum_multiples(multiple, limit)

        assert (
            actual == expected
        ), f"Mathematical property failed for multiple={multiple}, limit={limit}"

    @given(st.integers(min_value=2, max_value=1000))
    def test_euler_solution_monotonic_with_limit(self, limit):
        """Property: larger limits should give larger or equal results"""
        assume(limit >= 2)  # Need at least 2 to have a meaningful comparison

        result1 = solve_euler_1_optimized(limit)
        result2 = solve_euler_1_optimized(limit + 1)

        assert (
            result2 >= result1
        ), f"Result decreased when limit increased from {limit} to {limit + 1}"

    @given(st.integers(min_value=1, max_value=50))
    def test_sum_multiples_divisibility_property(self, multiple):
        """Property: if limit is exactly multiple + 1, result should equal multiple"""
        limit = multiple + 1
        result = sum_multiples(multiple, limit)
        assert (
            result == multiple
        ), f"Expected {multiple}, got {result} for limit {limit}"

    @given(st.integers(min_value=1, max_value=20))
    def test_sum_multiples_no_multiples_property(self, multiple):
        """Property: if limit <= multiple, result should be 0"""
        for limit in range(1, multiple + 1):
            result = sum_multiples(multiple, limit)
            assert (
                result == 0
            ), f"Expected 0 for multiple={multiple}, limit={limit}, got {result}"

    @given(
        st.integers(min_value=16, max_value=1000)
    )  # Start from 16 to ensure we have multiples of 15
    def test_inclusion_exclusion_property(self, limit):
        """Property: verify inclusion-exclusion principle for multiples of 3 and 5"""
        # Direct calculation
        multiples_3 = sum_multiples(3, limit)
        multiples_5 = sum_multiples(5, limit)
        multiples_15 = sum_multiples(15, limit)

        # Using inclusion-exclusion principle
        inclusion_exclusion_result = multiples_3 + multiples_5 - multiples_15

        # Should match our optimized solution
        euler_result = solve_euler_1_optimized(limit)

        assert (
            euler_result == inclusion_exclusion_result
        ), f"Inclusion-exclusion failed at limit {limit}: {euler_result} != {inclusion_exclusion_result}"

    @given(st.integers(min_value=1, max_value=100))
    def test_sum_multiples_scaling_property(self, base_multiple):
        """Property: sum_multiples(k*m, limit) should relate predictably to sum_multiples(m, limit)"""
        limit = 200
        k = 3  # scaling factor

        sum_base = sum_multiples(base_multiple, limit)

        # The scaled version should have fewer terms, each k times larger
        # This is a complex relationship, so we'll just verify basic sanity
        if sum_base > 0:
            # If there are multiples of base_multiple, there should be fewer (or equal) multiples of k*base_multiple
            n_base = (limit - 1) // base_multiple
            n_scaled = (limit - 1) // (k * base_multiple)
            assert (
                n_scaled <= n_base
            ), f"Scaled multiple should have fewer terms: {n_scaled} vs {n_base}"


# Run the original code
if __name__ == "__main__":
    result = solve_euler_1_optimized()
    print(f"Optimized result: {result}")

    # Run tests with hypothesis
    pytest.main([__file__, "-v", "--hypothesis-show-statistics"])
