# Build Roadmap

The order below is a dependency order. Black-Scholes came first because every
other module is defined in terms of it: the Greeks are its derivatives, implied
vol is its inverse, and the tree and Monte Carlo pricers are checked against it.
The IV surface came last since it uses everything else.

## Checklist

### 1. Black-Scholes (`black_scholes.py`)
- [x] `d1(...)` (sanity: canonical set gives 0.35)
- [x] `d2(...)` (sanity: canonical set gives 0.15)
- [x] `black_scholes_price(...)` call & put branches
- [x] `pytest tests/test_black_scholes.py -v` all green

### 2. Greeks (`greeks.py`)
- [x] `delta(...)`
- [x] `gamma(...)`
- [x] `vega(...)`
- [x] `theta(...)`
- [x] `rho(...)`
- [x] `pytest tests/test_greeks.py -v` all green (known-value and finite-difference)

### 3. Implied volatility (`implied_vol.py`)
- [x] `implied_volatility(...)` objective + bracketing + Brent solve
- [x] `pytest tests/test_implied_vol.py -v` all green (round trips)

### 4. Binomial tree (`binomial.py`)
- [x] `binomial_price(...)` terminal payoffs + backward induction (European)
- [x] American early-exercise branch (`max(continuation, intrinsic)`)
- [x] `pytest tests/test_binomial.py -v` all green (converges to BS; American put >= European)

### 5. Monte Carlo (`monte_carlo.py`)
- [x] `monte_carlo_price(...)` GBM terminal simulation + discounted payoff
- [x] antithetic-variates path
- [x] standard-error calculation returning `MCResult`
- [x] `pytest tests/test_monte_carlo.py -v` all green (near BS; se scales with 1/sqrt(n); antithetic reduces variance)

### 6. Market data (`market_data.py`)
- [x] `load_options_chain(...)`
- [x] `pytest tests/test_market_data.py -v` all green

### 7. IV surface (`surface.py`)
- [x] `build_iv_surface(...)` invert each quote into a strike x expiry grid
- [x] `plot_iv_surface(...)` 3D `plot_surface`
- [x] `pytest tests/test_surface.py -v` all green (flat-surface round trip)

### Wrap-up
- [x] Whole suite green: `pytest`
- [x] CI green on GitHub (Actions runs `pytest` on push)
