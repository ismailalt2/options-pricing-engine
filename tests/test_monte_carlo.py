"""Tests for the Monte Carlo pricer.

Stochastic output, so the checks are statistical: near Black-Scholes,
standard error ~ 1/sqrt(n), antithetic beats plain MC. Fixed seeds keep
every run deterministic.
"""

import math

import pytest

import reference_values as ref
from options_pricing.black_scholes import black_scholes_price
from options_pricing.monte_carlo import monte_carlo_price


@pytest.mark.parametrize("kind", ["call", "put"])
def test_estimate_near_black_scholes(kind):
    bs = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, kind)
    res = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, kind,
        n_paths=400_000, antithetic=True, seed=12345,
    )
    # Within a tight absolute band AND within ~4 standard errors.
    assert res.price == pytest.approx(bs, abs=0.05)
    assert abs(res.price - bs) <= 4 * res.std_error


def test_confidence_interval_brackets_true_price():
    bs = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call")
    res = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call",
        n_paths=400_000, antithetic=True, seed=7,
    )
    lo, hi = res.confidence_interval(z=3.0)
    assert lo <= bs <= hi


def test_standard_error_scales_like_one_over_sqrt_n():
    # Use plain MC (no antithetic) so the 1/sqrt(n) law is clean.
    small = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call",
        n_paths=50_000, antithetic=False, seed=1,
    )
    big = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call",
        n_paths=200_000, antithetic=False, seed=1,
    )
    # 4x the paths -> ~2x smaller standard error.
    ratio = small.std_error / big.std_error
    assert ratio == pytest.approx(2.0, rel=0.25)


def test_antithetic_reduces_variance():
    plain = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call",
        n_paths=100_000, antithetic=False, seed=99,
    )
    anti = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call",
        n_paths=100_000, antithetic=True, seed=99,
    )
    assert anti.std_error < plain.std_error


def test_reproducible_with_seed():
    kwargs = dict(n_paths=50_000, antithetic=True, seed=2024)
    a = monte_carlo_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", **kwargs)
    b = monte_carlo_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", **kwargs)
    assert a.price == b.price
    assert a.std_error == b.std_error


def test_standard_error_is_positive():
    res = monte_carlo_price(
        ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call", n_paths=10_000, seed=0
    )
    assert res.std_error > 0
    assert math.isfinite(res.std_error)
