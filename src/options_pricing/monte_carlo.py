from __future__ import annotations
import numpy as np
from dataclasses import dataclass

from .validation import (
    validate_nonnegative,
    validate_option_type,
    validate_positive,
    validate_positive_int,
)


@dataclass(frozen=True)
class MCResult:
    price: float
    std_error: float
    n_paths: int

    def confidence_interval(self, z: float = 1.96) -> tuple[float, float]:
        half_width = z * self.std_error
        return (self.price - half_width, self.price + half_width)


def monte_carlo_price(
    S: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    option_type: str,
    n_paths: int = 100_000,
    antithetic: bool = True,
    q: float = 0.0,
    seed: int | None = None,
) -> MCResult:
    """European option price by simulating S_T directly (exact GBM step)."""
    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    validate_positive_int("n_paths", n_paths)
    option_type = validate_option_type(option_type)

    rng = np.random.default_rng(seed)

    if antithetic:
        half = (n_paths + 1) // 2
        z = rng.standard_normal(half)
        z = np.concatenate([z, -z])
    else:
        z = rng.standard_normal(n_paths)

    drift = (r - q - sigma**2 / 2) * T
    S_T = S * np.exp(drift + sigma * np.sqrt(T) * z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0.0)
    else:
        payoffs = np.maximum(K - S_T, 0.0)

    payoffs = np.exp(-r * T) * payoffs

    if antithetic:
        # average each Z with its mirror -Z, then treat the pairs as the samples
        pairs = (payoffs[:half] + payoffs[half:]) / 2
        price = pairs.mean()
        std_error = pairs.std(ddof=1) / np.sqrt(half)
    else:
        price = payoffs.mean()
        std_error = payoffs.std(ddof=1) / np.sqrt(len(payoffs))

    return MCResult(price=float(price), std_error=float(std_error), n_paths=len(z))
