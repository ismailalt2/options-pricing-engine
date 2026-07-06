"""Tests for the Black-Scholes closed-form pricer."""

import math

import pytest

import reference_values as ref
from options_pricing.black_scholes import black_scholes_price, d1, d2


# --- d1 / d2 exact values -------------------------------------------------

def test_d1_canonical():
    assert d1(ref.S, ref.K, ref.R, ref.SIGMA, ref.T) == pytest.approx(ref.D1, abs=1e-12)


def test_d2_canonical():
    assert d2(ref.S, ref.K, ref.R, ref.SIGMA, ref.T) == pytest.approx(ref.D2, abs=1e-12)


def test_d2_equals_d1_minus_sigma_root_t():
    got = d2(ref.S, ref.K, ref.R, ref.SIGMA, ref.T)
    expected = d1(ref.S, ref.K, ref.R, ref.SIGMA, ref.T) - ref.SIGMA * math.sqrt(ref.T)
    assert got == pytest.approx(expected, abs=1e-12)


# --- Known textbook prices ------------------------------------------------

def test_call_known_value():
    price = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call")
    assert price == pytest.approx(10.4506, abs=1e-4)


def test_put_known_value():
    price = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "put")
    assert price == pytest.approx(5.5735, abs=1e-4)


def test_call_full_precision():
    price = black_scholes_price(ref.S, ref.K, ref.R, ref.SIGMA, ref.T, "call")
    assert price == pytest.approx(ref.CALL_PRICE, rel=1e-10)


# --- Put-call parity: C - P = S*e^{-qT} - K*e^{-rT} -----------------------

@pytest.mark.parametrize(
    "S,K,r,sigma,T,q",
    [
        (100, 100, 0.05, 0.20, 1.0, 0.0),
        (120, 100, 0.03, 0.35, 0.5, 0.0),
        (90, 110, 0.01, 0.15, 2.0, 0.02),
        (100, 100, -0.01, 0.25, 0.75, 0.0),
    ],
)
def test_put_call_parity(S, K, r, sigma, T, q):
    call = black_scholes_price(S, K, r, sigma, T, "call", q=q)
    put = black_scholes_price(S, K, r, sigma, T, "put", q=q)
    lhs = call - put
    rhs = S * math.exp(-q * T) - K * math.exp(-r * T)
    assert lhs == pytest.approx(rhs, abs=1e-10)


# --- Sanity / boundary behaviour -----------------------------------------

def test_call_price_at_least_intrinsic():
    # A call is worth at least its discounted intrinsic value; always >= 0.
    price = black_scholes_price(150, 100, 0.05, 0.20, 1.0, "call")
    assert price >= 150 - 100 * math.exp(-0.05)


def test_prices_are_positive():
    assert black_scholes_price(100, 100, 0.05, 0.20, 1.0, "call") > 0
    assert black_scholes_price(100, 100, 0.05, 0.20, 1.0, "put") > 0


# --- Input validation --------------------------------------------------

def test_rejects_bad_option_type():
    with pytest.raises(ValueError):
        black_scholes_price(100, 100, 0.05, 0.20, 1.0, "banana")


def test_rejects_nonpositive_sigma():
    with pytest.raises(ValueError):
        black_scholes_price(100, 100, 0.05, 0.0, 1.0, "call")
