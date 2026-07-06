
from __future__ import annotations
import numpy as np
from scipy.optimize import brentq
from .black_scholes import black_scholes_price

from .validation import (
    validate_nonnegative,
    validate_option_type,
    validate_positive,
)


def implied_volatility(market_price: float,S: float,K: float,r: float,T: float,option_type: str,q: float = 0.0,sigma_low: float = 1e-6,sigma_high: float = 5.0,tol: float = 1e-8,max_iter: int = 100,
                       ):

    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    option_type = validate_option_type(option_type)
    if market_price <= 0:
        raise ValueError(f"market_price must be positive, got {market_price!r}")

    def objective(sigma):
        model_price = black_scholes_price(
            S=S,
            K=K,
            r=r,
            sigma=sigma,
            T=T,
            option_type=option_type,
            q=q,
        )

        return model_price - market_price
    

    f_low = objective(sigma_low)
    f_high = objective(sigma_high)

    if f_low * f_high > 0:
        raise ValueError(
            "Unable to bracket the implied volatility "
            "with the supplied sigma range.")
    

    implied_vol = brentq(
        objective,
        sigma_low,
        sigma_high,
        xtol=tol,
        maxiter=max_iter,
    )

    return implied_vol
