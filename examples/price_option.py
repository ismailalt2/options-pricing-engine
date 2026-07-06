#!/usr/bin/env python3
"""Price a single option from the command line and print its Greeks.

Example:
    python examples/price_option.py -S 100 -K 100 -r 0.05 --sigma 0.20 -T 1 --type call
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# make the src/ layout importable without an install
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from options_pricing.black_scholes import black_scholes_price  # noqa: E402
from options_pricing.binomial import binomial_price  # noqa: E402
from options_pricing.greeks import delta, gamma, rho, theta, vega  # noqa: E402
from options_pricing.monte_carlo import monte_carlo_price  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Price a European option and show Greeks.")
    p.add_argument("-S", "--spot", type=float, required=True, help="Underlying spot price")
    p.add_argument("-K", "--strike", type=float, required=True, help="Strike price")
    p.add_argument("-r", "--rate", type=float, required=True, help="Risk-free rate (e.g. 0.05)")
    p.add_argument("--sigma", type=float, required=True, help="Volatility (e.g. 0.20)")
    p.add_argument("-T", "--maturity", type=float, required=True, help="Time to expiry in years")
    p.add_argument("--type", choices=["call", "put"], default="call", help="Option type")
    p.add_argument("-q", "--dividend", type=float, default=0.0, help="Dividend yield")
    p.add_argument(
        "--method",
        choices=["bs", "binomial", "mc"],
        default="bs",
        help="Pricing method (bs = Black-Scholes closed form)",
    )
    p.add_argument("--steps", type=int, default=500, help="Binomial tree steps")
    p.add_argument("--paths", type=int, default=100_000, help="Monte Carlo paths")
    p.add_argument(
        "--exercise",
        choices=["european", "american"],
        default="european",
        help="Exercise style (binomial only)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    S, K, r, sig, T, q = args.spot, args.strike, args.rate, args.sigma, args.maturity, args.dividend
    kind = args.type

    if args.method == "bs":
        price = black_scholes_price(S, K, r, sig, T, kind, q=q)
    elif args.method == "binomial":
        price = binomial_price(S, K, r, sig, T, kind, exercise=args.exercise, steps=args.steps, q=q)
    else:  # mc
        result = monte_carlo_price(S, K, r, sig, T, kind, n_paths=args.paths, q=q, seed=0)
        price = result.price

    print(f"\n{kind.upper()} option  (method={args.method})")
    print(f"  S={S}  K={K}  r={r}  sigma={sig}  T={T}  q={q}")
    print(f"  price = {price:.6f}")

    if args.method == "mc":
        print(f"  std_error = {result.std_error:.6f}")

    # analytic Greeks only make sense for the closed-form model
    if args.method == "bs":
        print("  Greeks:")
        print(f"    delta = {delta(S, K, r, sig, T, kind, q=q):+.6f}")
        print(f"    gamma = {gamma(S, K, r, sig, T, q=q):+.6f}")
        print(f"    vega  = {vega(S, K, r, sig, T, q=q):+.6f}  (per 1.00 vol)")
        print(f"    theta = {theta(S, K, r, sig, T, kind, q=q):+.6f}  (per year)")
        print(f"    rho   = {rho(S, K, r, sig, T, kind, q=q):+.6f}  (per 1.00 rate)")
    print()
    return 0


if __name__ == "__main__":
    main()
