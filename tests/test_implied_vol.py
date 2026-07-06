"""Tests for the implied-volatility solver. Core property: it inverts the pricer."""

import pytest

import reference_values as ref
from options_pricing.black_scholes import black_scholes_price
from options_pricing.implied_vol import implied_volatility


@pytest.mark.parametrize("kind", ["call", "put"])
@pytest.mark.parametrize("sigma_true", [0.10, 0.20, 0.35, 0.60])
def test_recovers_known_sigma(kind, sigma_true):
    # Build a price from a known sigma, then invert it back to that sigma.
    market = black_scholes_price(ref.S, ref.K, ref.R, sigma_true, ref.T, kind)
    iv = implied_volatility(market, ref.S, ref.K, ref.R, ref.T, kind)
    assert iv == pytest.approx(sigma_true, abs=1e-4)


@pytest.mark.parametrize("kind", ["call", "put"])
def test_price_round_trip(kind):
    # price -> IV -> price must return the original price.
    market = black_scholes_price(ref.S, 110, ref.R, 0.28, ref.T, kind)
    iv = implied_volatility(market, ref.S, 110, ref.R, ref.T, kind)
    repriced = black_scholes_price(ref.S, 110, ref.R, iv, ref.T, kind)
    assert repriced == pytest.approx(market, abs=1e-6)


def test_recovers_sigma_off_the_money():
    # A deep OTM option still round-trips (bracketing must be wide enough).
    kind = "call"
    market = black_scholes_price(100, 140, 0.05, 0.45, 0.5, kind)
    iv = implied_volatility(market, 100, 140, 0.05, 0.5, kind)
    assert iv == pytest.approx(0.45, abs=1e-4)


def test_rejects_nonpositive_price():
    with pytest.raises(ValueError):
        implied_volatility(0.0, 100, 100, 0.05, 1.0, "call")
