"""Tests for the CRR binomial tree pricer.

European prices must converge to Black-Scholes, and the American
early-exercise rules must hold (call w/o dividends = European, put >= European).
"""

import pytest

import reference_values as ref
from options_pricing.binomial import binomial_price
from options_pricing.black_scholes import black_scholes_price


@pytest.mark.parametrize("kind", ["call", "put"])
def test_european_converges_to_black_scholes(kind):
    bs = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, kind)
    tree = binomial_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, kind, exercise="european", steps=1000
    )
    # CRR error is O(1/steps); 1000 steps comfortably inside 0.02.
    assert tree == pytest.approx(bs, abs=0.02)


def test_convergence_improves_with_more_steps():
    bs = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call")
    coarse = binomial_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", steps=25)
    fine = binomial_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", steps=1000)
    assert abs(fine - bs) < abs(coarse - bs)


def test_american_call_equals_european_call_no_dividend():
    # q = 0: never optimal to exercise an American call early, so prices match.
    eu = binomial_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", "european", 500)
    am = binomial_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", "american", 500)
    assert am == pytest.approx(eu, abs=1e-8)


def test_american_put_at_least_european_put():
    eu = binomial_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "put", "european", 500)
    am = binomial_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "put", "american", 500)
    assert am >= eu - 1e-9


def test_american_put_strictly_greater_when_deep_itm():
    # Deep in-the-money put with meaningful rate: early exercise is valuable.
    args = (60.0, 100.0, 0.08, 0.20, 1.0, "put")
    eu = binomial_price(*args, exercise="european", steps=500)
    am = binomial_price(*args, exercise="american", steps=500)
    assert am > eu


def test_rejects_bad_exercise_style():
    with pytest.raises(ValueError):
        binomial_price(100, 100, 0.05, 0.2, 1.0, "call", exercise="bermudan")
