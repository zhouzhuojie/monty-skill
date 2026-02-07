"""Tests for monty sandbox."""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).parent
MONTY = [sys.executable, str(SCRIPT_DIR / "monty.py")]


def run_monty(code: str, functions_file: str = "functions.py") -> tuple[int, str]:
    """Run monty with given code and return (exit_code, output)."""
    result = subprocess.run(
        [*MONTY, code, "-f", functions_file],
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR,
    )
    return result.returncode, result.stdout.strip()


def run_monty_error(code: str) -> bool:
    """Check if code produces an error."""
    exit_code, _ = run_monty(code)
    return exit_code != 0


class TestBasicArithmetic:
    def test_addition(self):
        code, out = run_monty("print(2 + 2)")
        assert code == 0 and out == "4"

    def test_multiplication(self):
        code, out = run_monty("print(10 * 10)")
        assert code == 0 and out == "100"

    def test_division(self):
        code, out = run_monty("print(10 / 2)")
        assert code == 0 and out == "5.0"

    def test_integer_division(self):
        code, out = run_monty("print(10 // 2)")
        assert code == 0 and out == "5"

    def test_modulo(self):
        code, out = run_monty("print(10 % 3)")
        assert code == 0 and out == "1"

    def test_exponentiation(self):
        code, out = run_monty("print(10 ** 2)")
        assert code == 0 and out == "100"


class TestVariables:
    def test_simple_assignment(self):
        code, out = run_monty("x = 42; print(x)")
        assert code == 0 and out == "42"

    def test_multiple_variables(self):
        code, out = run_monty("a = 10; b = 20; print(a + b)")
        assert code == 0 and out == "30"


class TestBuiltins:
    def test_len_list(self):
        code, out = run_monty("print(len([1, 2, 3, 4, 5]))")
        assert code == 0 and out == "5"

    def test_len_string(self):
        code, out = run_monty("print(len('hello'))")
        assert code == 0 and out == "5"

    def test_int_function(self):
        code, out = run_monty("print(int('42'))")
        assert code == 0 and out == "42"

    def test_float_function(self):
        code, out = run_monty("print(float(3))")
        assert code == 0 and out == "3.0"

    def test_bool_function(self):
        code, out = run_monty("print(bool(1))")
        assert code == 0 and out == "True"


class TestRangeAndIteration:
    def test_range(self):
        code, out = run_monty("print(list(range(5)))")
        assert code == 0 and out == "[0, 1, 2, 3, 4]"

    def test_enumerate(self):
        code, out = run_monty("print(list(enumerate(['a', 'b', 'c'])))")
        assert code == 0 and out == "[(0, 'a'), (1, 'b'), (2, 'c')]"

    def test_zip(self):
        code, out = run_monty("print(list(zip([1, 2], ['a', 'b'])))")
        assert code == 0 and out == "[(1, 'a'), (2, 'b')]"


class TestListComprehensions:
    def test_simple(self):
        code, out = run_monty("print([x for x in range(5)])")
        assert code == 0 and out == "[0, 1, 2, 3, 4]"

    def test_with_condition(self):
        code, out = run_monty("print([x for x in range(10) if x % 2 == 1])")
        assert code == 0 and out == "[1, 3, 5, 7, 9]"


class TestLambdaFunctions:
    def test_simple_lambda(self):
        code, out = run_monty("f = lambda x: x * 2; print(f(5))")
        assert code == 0 and out == "10"


class TestTypeHints:
    def test_variable_type_hint(self):
        code, out = run_monty("x: int = 42; print(x)")
        assert code == 0 and out == "42"


class TestStringOperations:
    def test_concat(self):
        code, out = run_monty("print('hello' + 'world')")
        assert code == 0 and out == "helloworld"

    def test_fstring(self):
        code, out = run_monty("name = 'world'; print(f'hello {name}')")
        assert code == 0 and out == "hello world"


class TestExternalFunctions:
    def test_greet(self):
        code, out = run_monty("print(await greet('World'))")
        assert code == 0 and out == "Hello, World!"

    def test_calculate_add(self):
        code, out = run_monty("print(await calculate(5, 3, 'add'))")
        assert code == 0 and out == "8"

    def test_calculate_mul(self):
        code, out = run_monty("print(await calculate(5, 3, 'mul'))")
        assert code == 0 and out == "15"

    def test_capitalize(self):
        code, out = run_monty("print(await capitalize('hello'))")
        assert code == 0 and out == "Hello"

    def test_reverse(self):
        code, out = run_monty("print(await reverse('hello'))")
        assert code == 0 and out == "olleh"


class TestComplexCombinations:
    def test_list_comp_sum(self):
        code, out = run_monty("print(sum([x ** 2 for x in range(1, 16)]))")
        assert code == 0 and out == "1240"


class TestCustomExternalFunctions:
    """Tests for user-defined external functions in functions.py."""

    def test_random_numbers_count(self):
        """Test that random_numbers returns correct count."""
        code, out = run_monty("print(len(random_numbers(100)))")
        assert code == 0 and out == "100"

    def test_random_numbers_range(self):
        """Test that random numbers are between 0 and 1."""
        code, out = run_monty("nums = random_numbers(100); print(min(nums) >= 0 and max(nums) <= 1)")
        assert code == 0 and out == "True"

    def test_random_numbers_mean(self):
        """Test that mean of 1000 random numbers is approximately 0.5."""
        code, out = run_monty("nums = random_numbers(1000); mean = sum(nums)/len(nums); print(0.4 <= mean <= 0.6)")
        assert code == 0 and out == "True"

    def test_random_int_count(self):
        """Test that random_int returns correct count."""
        code, out = run_monty("print(len(random_int(1, 10, 50)))")
        assert code == 0 and out == "50"

    def test_random_int_range(self):
        """Test that random integers are within specified range."""
        code, out = run_monty("nums = random_int(1, 6, 100); print(min(nums) >= 1 and max(nums) <= 6)")
        assert code == 0 and out == "True"


class TestErrorCases:
    def test_syntax_error(self):
        assert run_monty_error("print(")

    def test_undefined_variable(self):
        assert run_monty_error("print(undefined_variable)")

    def test_division_by_zero(self):
        assert run_monty_error("print(1 / 0)")

    def test_index_error(self):
        assert run_monty_error("print([1, 2][10])")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
