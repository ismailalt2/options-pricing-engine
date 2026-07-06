"""Tests for IV surface construction and plotting.

Main check is the flat-surface round trip: prices generated from one constant
sigma must invert back to that sigma in every grid cell.
"""

import matplotlib

matplotlib.use("Agg")  # redundant with conftest, but keeps this file standalone

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from options_pricing.black_scholes import black_scholes_price
from options_pricing.surface import build_iv_surface, plot_iv_surface

SIGMA_FLAT = 0.20
STRIKES = [80, 90, 100, 110, 120]
EXPIRIES = [0.25, 0.5, 1.0]
S, R = 100.0, 0.05


def _synthetic_flat_chain():
    """Chain where every call price comes from the same constant sigma."""
    rows = []
    for T in EXPIRIES:
        for K in STRIKES:
            rows.append(
                {
                    "underlying_price": S,
                    "strike": float(K),
                    "option_type": "call",
                    "market_price": black_scholes_price(S, K, R, SIGMA_FLAT, T, "call"),
                    "risk_free_rate": R,
                    "dividend_yield": 0.0,
                    "time_to_expiry": T,
                }
            )
    return pd.DataFrame(rows)


def test_flat_surface_round_trip():
    chain = _synthetic_flat_chain()
    surface = build_iv_surface(chain, option_type="call")
    assert isinstance(surface, pd.DataFrame)
    # Every recovered IV equals the constant sigma used to generate the prices.
    values = surface.to_numpy().ravel()
    for iv in values:
        assert iv == pytest.approx(SIGMA_FLAT, abs=1e-4)


def test_surface_grid_shape():
    chain = _synthetic_flat_chain()
    surface = build_iv_surface(chain, option_type="call")
    # strikes on one axis, expiries on the other
    assert set(surface.shape) == {len(STRIKES), len(EXPIRIES)}


def test_plot_returns_axes_with_surface():
    # Feed a ready-made IV grid so this test isolates the plotting code.
    grid = pd.DataFrame(
        [[0.22, 0.20, 0.19], [0.20, 0.18, 0.17], [0.21, 0.19, 0.18]],
        index=[90, 100, 110],
        columns=[0.25, 0.5, 1.0],
    )
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    returned = plot_iv_surface(grid, ax=ax)
    assert returned is not None
    # plot_surface adds a 3D collection to the axes.
    assert len(returned.collections) >= 1
    plt.close(fig)
