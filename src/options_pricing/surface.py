from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .implied_vol import implied_volatility
from .validation import validate_option_type


def build_iv_surface(chain: pd.DataFrame, option_type: str = "call") -> pd.DataFrame:
    """Invert every quote in the chain and pivot into a strike x expiry grid."""
    option_type = validate_option_type(option_type)
    data = chain[chain["option_type"] == option_type].copy()

    ivs = []
    for row in data.itertuples():
        try:
            iv = implied_volatility(
                row.market_price,
                row.underlying_price,
                row.strike,
                row.risk_free_rate,
                row.time_to_expiry,
                option_type,
                q=row.dividend_yield,
            )
        except ValueError:
            iv = np.nan  # price outside no-arbitrage bounds, leave a hole
        ivs.append(iv)

    data["implied_vol"] = ivs
    return data.pivot_table(index="strike", columns="time_to_expiry", values="implied_vol")


def plot_iv_surface(surface: pd.DataFrame, title: str = "Implied Volatility Surface", ax=None):
    if ax is None:
        fig = plt.figure(figsize=(9, 6))
        ax = fig.add_subplot(projection="3d")

    strikes = surface.index.to_numpy(dtype=float)
    expiries = surface.columns.to_numpy(dtype=float)
    X, Y = np.meshgrid(expiries, strikes)
    Z = np.ma.masked_invalid(surface.to_numpy(dtype=float))

    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_xlabel("Time to expiry (yrs)")
    ax.set_ylabel("Strike")
    ax.set_zlabel("Implied vol")
    ax.set_title(title)
    return ax
