"""Tests for the options-chain CSV loader."""

from pathlib import Path

import pytest

from options_pricing.market_data import REQUIRED_COLUMNS, load_options_chain

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "data" / "sample_options_chain.csv"


def test_sample_file_exists():
    assert SAMPLE_CSV.exists(), "data/sample_options_chain.csv is missing"


def test_loads_sample_chain():
    df = load_options_chain(str(SAMPLE_CSV))
    assert len(df) > 0
    for col in REQUIRED_COLUMNS:
        assert col in df.columns


def test_adds_time_to_expiry_column():
    df = load_options_chain(str(SAMPLE_CSV))
    assert "time_to_expiry" in df.columns
    assert (df["time_to_expiry"] > 0).all()


def test_adds_dividend_yield_when_absent(tmp_path):
    csv = tmp_path / "no_div.csv"
    csv.write_text(
        "quote_date,expiry_date,underlying_price,strike,option_type,market_price,risk_free_rate\n"
        "2026-06-30,2026-12-31,100,100,call,8.2,0.05\n"
    )
    df = load_options_chain(str(csv))
    assert "dividend_yield" in df.columns
    assert df["dividend_yield"].iloc[0] == 0.0


def test_option_type_normalised(tmp_path):
    csv = tmp_path / "mixed_case.csv"
    csv.write_text(
        "quote_date,expiry_date,underlying_price,strike,option_type,market_price,risk_free_rate\n"
        "2026-06-30,2026-12-31,100,100,CALL,8.2,0.05\n"
        "2026-06-30,2026-12-31,100,100,Put,4.1,0.05\n"
    )
    df = load_options_chain(str(csv))
    assert set(df["option_type"]) == {"call", "put"}


def test_missing_column_raises(tmp_path):
    csv = tmp_path / "bad.csv"
    csv.write_text("quote_date,strike\n2026-06-30,100\n")
    with pytest.raises(ValueError):
        load_options_chain(str(csv))


def test_expiry_before_quote_raises(tmp_path):
    csv = tmp_path / "backwards.csv"
    csv.write_text(
        "quote_date,expiry_date,underlying_price,strike,option_type,market_price,risk_free_rate\n"
        "2026-12-31,2026-06-30,100,100,call,8.2,0.05\n"
    )
    with pytest.raises(ValueError):
        load_options_chain(str(csv))
