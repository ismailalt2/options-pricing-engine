"""Tests for the analytic Greeks: known values plus finite-difference checks.

Conventions: vega and rho are per unit, theta is per year.
"""

import pytest

import reference_values as ref
from options_pricing.black_scholes import black_scholes_price
from options_pricing.greeks import delta, gamma, rho, theta, vega

# Canonical params as a tuple for convenience.
P = (ref.S, ref.K, ref.R, ref.SIGMA, ref.T)


def price(S=ref.S, K=ref.K, r=ref.R, sigma=ref.SIGMA, T=ref.T, kind="call", q=0.0):
    return black_scholes_price(S, K, r, sigma, T, kind, q=q)


# --- Known analytic values ------------------------------------------------

def test_delta_call_known():
    assert delta(*P, "call") == pytest.approx(ref.DELTA_CALL, abs=1e-6)


def test_delta_put_known():
    assert delta(*P, "put") == pytest.approx(ref.DELTA_PUT, abs=1e-6)


def test_gamma_known():
    assert gamma(*P) == pytest.approx(ref.GAMMA, abs=1e-8)


def test_vega_known():
    assert vega(*P) == pytest.approx(ref.VEGA, abs=1e-5)


def test_theta_call_known():
    assert theta(*P, "call") == pytest.approx(ref.THETA_CALL, abs=1e-5)


def test_theta_put_known():
    assert theta(*P, "put") == pytest.approx(ref.THETA_PUT, abs=1e-5)


def test_rho_call_known():
    assert rho(*P, "call") == pytest.approx(ref.RHO_CALL, abs=1e-5)


def test_rho_put_known():
    assert rho(*P, "put") == pytest.approx(ref.RHO_PUT, abs=1e-5)


# --- Delta/put relationship ----------------------------------------------

def test_delta_call_minus_put_is_one_no_dividend():
    # With q = 0: delta_call - delta_put = 1 exactly.
    assert delta(*P, "call") - delta(*P, "put") == pytest.approx(1.0, abs=1e-10)


def test_gamma_same_for_call_and_put():
    # gamma is identical for calls and puts, hence no option_type argument
    assert gamma(*P) >= 0


# --- Finite-difference cross-checks (central differences) -----------------

@pytest.mark.parametrize("kind", ["call", "put"])
def test_delta_matches_finite_difference(kind):
    h = 1e-4 * ref.S
    fd = (price(S=ref.S + h, kind=kind) - price(S=ref.S - h, kind=kind)) / (2 * h)
    assert delta(*P, kind) == pytest.approx(fd, rel=1e-4, abs=1e-6)


@pytest.mark.parametrize("kind", ["call", "put"])
def test_gamma_matches_second_difference(kind):
    h = 0.1
    fd = (
        price(S=ref.S + h, kind=kind)
        - 2 * price(S=ref.S, kind=kind)
        + price(S=ref.S - h, kind=kind)
    ) / (h * h)
    assert gamma(*P) == pytest.approx(fd, rel=1e-3, abs=1e-6)


@pytest.mark.parametrize("kind", ["call", "put"])
def test_vega_matches_finite_difference(kind):
    h = 1e-4
    fd = (price(sigma=ref.SIGMA + h, kind=kind) - price(sigma=ref.SIGMA - h, kind=kind)) / (2 * h)
    assert vega(*P) == pytest.approx(fd, rel=1e-4, abs=1e-4)


@pytest.mark.parametrize("kind", ["call", "put"])
def test_rho_matches_finite_difference(kind):
    h = 1e-5
    fd = (price(r=ref.R + h, kind=kind) - price(r=ref.R - h, kind=kind)) / (2 * h)
    assert rho(*P, kind) == pytest.approx(fd, rel=1e-4, abs=1e-4)


@pytest.mark.parametrize("kind", ["call", "put"])
def test_theta_matches_finite_difference(kind):
    # theta = dV/dt = -dV/dT.
    h = 1e-4
    fd = -(price(T=ref.T + h, kind=kind) - price(T=ref.T - h, kind=kind)) / (2 * h)
    assert theta(*P, kind) == pytest.approx(fd, rel=1e-3, abs=1e-3)
