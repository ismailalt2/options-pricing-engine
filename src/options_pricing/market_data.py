from __future__ import annotations
import pandas as pd

from .validation import CALL, PUT

REQUIRED_COLUMNS = (
    "quote_date",
    "expiry_date",
    "underlying_price",
    "strike",
    "option_type",
    "market_price",
    "risk_free_rate",
)

DAYS_PER_YEAR = 365.0


def load_options_chain(path: str) -> pd.DataFrame:
    """Load an options-chain CSV and add a time_to_expiry column in years."""
    df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    df = df.copy()
    df["quote_date"] = pd.to_datetime(df["quote_date"])
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])
    df["option_type"] = df["option_type"].astype(str).str.strip().str.lower()

    bad_types = set(df["option_type"].unique()) - {CALL, PUT}
    if bad_types:
        raise ValueError(f"option_type column has invalid values: {sorted(bad_types)}")

    if "dividend_yield" not in df.columns:
        df["dividend_yield"] = 0.0
    df["dividend_yield"] = df["dividend_yield"].fillna(0.0)

    df["time_to_expiry"] = (
        (df["expiry_date"] - df["quote_date"]).dt.days / DAYS_PER_YEAR
    )

    for col in ("underlying_price", "strike", "market_price"):
        if (df[col] <= 0).any():
            raise ValueError(f"column {col!r} contains non-positive values")
    if (df["time_to_expiry"] <= 0).any():
        raise ValueError("every row must have expiry_date strictly after quote_date")

    return df.reset_index(drop=True)
