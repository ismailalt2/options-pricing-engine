#!/usr/bin/env python3
"""Build the implied-vol surface from an options-chain CSV and save it as a PNG.

Example:
    python examples/plot_surface.py --out iv_surface.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib.pyplot as plt  # noqa: E402

from options_pricing.market_data import load_options_chain  # noqa: E402
from options_pricing.surface import build_iv_surface, plot_iv_surface  # noqa: E402

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "data" / "sample_options_chain.csv"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Plot an implied-vol surface from a chain CSV.")
    p.add_argument("csv", nargs="?", default=str(DEFAULT_CSV), help="Options-chain CSV path")
    p.add_argument("--type", choices=["call", "put"], default="call", help="Option type to plot")
    p.add_argument("--out", default="iv_surface.png", help="Output PNG path")
    args = p.parse_args(argv)

    chain = load_options_chain(args.csv)
    surface = build_iv_surface(chain, option_type=args.type)

    ax = plot_iv_surface(surface, title=f"Implied Volatility Surface ({args.type}s)")
    ax.figure.savefig(args.out, dpi=150, bbox_inches="tight")
    print(f"Saved surface plot to {args.out}")
    plt.close(ax.figure)
    return 0


if __name__ == "__main__":
    main()
