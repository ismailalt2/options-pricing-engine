from __future__ import annotations
import numpy as np

from .validation import (
    validate_exercise,
    validate_nonnegative,
    validate_option_type,
    validate_positive,
    validate_positive_int,
)


def binomial_price(
    S: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    option_type: str,
    exercise: str = "european",
    steps: int = 500,
    q: float = 0.0,
) -> float:
    """CRR binomial tree, backward induction. Handles european and american."""
    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    option_type = validate_option_type(option_type)
    exercise = validate_exercise(exercise)
    steps = validate_positive_int("steps", steps)

    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    a = np.exp((r - q) * dt)
    p = (a - d) / (u - d)
    disc = np.exp(-r * dt)

    j = np.arange(steps + 1)
    spots = S * u**j * d ** (steps - j)

    if option_type == "call":
        values = np.maximum(spots - K, 0.0)
    else:
        values = np.maximum(K - spots, 0.0)

    for _ in range(steps):
        values = disc * (p * values[1:] + (1 - p) * values[:-1])
        spots = spots[:-1] * u  # spots one step earlier
        if exercise == "american":
            if option_type == "call":
                values = np.maximum(values, spots - K)
            else:
                values = np.maximum(values, K - spots)

    return float(values[0])
