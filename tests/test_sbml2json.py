import pytest
from bionetgen.atomizer.sbml2json import factorial, comb


def test_comb():
    assert comb(5, 2) == 10
    assert comb(10, 3) == 120
    assert comb(10, 7) == 120
    assert comb(5, 0) == 1
    assert comb(5, 5) == 1
    assert comb(0, 0) == 1
    assert comb(1, 1) == 1
    assert comb(1, 0) == 1
    assert comb(5, 6) == 120 / 720


def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(5) == 120
    assert factorial(10) == 3628800

    # Also test negative number just in case
    # Currently the implementation behaves by returning 1 for negative numbers
    assert factorial(-1) == 1
