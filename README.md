# Options Pricing & Volatility Engine

A from-scratch options pricing toolkit built in Python for learning quantitative finance and numerical methods.

Every pricing model is implemented directly from the underlying mathematics, without using quantitative finance libraries such as QuantLib or `py_vollib`. The project focuses on understanding how pricing algorithms work rather than treating them as black boxes.

The implementation follows a test-driven approach, with mathematical correctness validated through unit tests and cross-checks between pricing models.

---

## Features

- Black-Scholes pricing for European call and put options
- Analytical Greeks (Delta, Gamma, Vega, Theta, Rho)
- Monte Carlo pricing with antithetic variates
- Cox-Ross-Rubinstein (CRR) binomial tree for European and American options
- Implied volatility solver using Brent's method
- IV surface generation from real options-chain data
- Command-line interface for pricing options and viewing Greeks

---

## Project Structure

```
examples/
├── price_option.py
└── plot_surface.py

src/options_pricing/
├── black_scholes.py
├── greeks.py
├── implied_vol.py
├── binomial.py
├── monte_carlo.py
├── market_data.py
├── surface.py
└── validation.py

tests/
docs/
```

Core dependency graph:

```
Black-Scholes
     │
     ├── Greeks
     ├── Implied Volatility
     ├── Monte Carlo (validation)
     └── Binomial Tree (validation)

Market Data
     │
     └── IV Surface
```

---

## Installation

Requires Python 3.10 or newer.

```bash
git clone <your-repository-url>
cd options-pricing-engine

python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Usage

### Black-Scholes

```bash
python examples/price_option.py \
    -S 100 \
    -K 100 \
    -r 0.05 \
    --sigma 0.20 \
    -T 1 \
    --type call
```

### Binomial Tree

```bash
python examples/price_option.py \
    --method binomial \
    --steps 500 \
    -S 100 \
    -K 100 \
    -r 0.05 \
    --sigma 0.20 \
    -T 1 \
    --type call
```

### Monte Carlo

```bash
python examples/price_option.py \
    --method mc \
    --paths 200000 \
    -S 100 \
    -K 100 \
    -r 0.05 \
    --sigma 0.20 \
    -T 1 \
    --type call
```

### Generate an IV Surface

```bash
python examples/plot_surface.py --out iv_surface.png
```

---

## Running Tests

Run the full test suite:

```bash
pytest
```

Or test a specific module:

```bash
pytest tests/test_black_scholes.py -v
```

---

## Current Progress

| Module | Status  |
|--------| --------|
| Black-Scholes |✅ Complete|
| Greeks |✅ Complete|
| Implied Volatility |✅ Complete|
| Binomial Tree |✅ Complete|
| Monte Carlo |✅ Complete|
| Market Data Loader |✅ Complete|
| IV Surface |✅ Complete|
| Validation Utilities |✅ Complete|

---

## Reference Values

Using:

- Spot Price = 100
- Strike = 100
- Risk-Free Rate = 5%
- Volatility = 20%
- Time to Expiry = 1 year

| Quantity | Value |
|-----------|------:|
| Call Price | 10.4506 |
| Put Price | 5.5735 |
| Call Delta | 0.6368 |
| Gamma | 0.018762 |
| Vega | 37.524 |
| Theta | -6.414 |
| Rho | 53.232 |

---

## Documentation

Additional project documentation is available in the `docs/` directory.

- **ROADMAP.md**: implementation plan
- **RESOURCES.md**: references and study material
- **NOTES.md**: learning notes

---

## License

Released under the MIT License.
