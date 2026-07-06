# Learning Path & Resources

Primary reference for the whole project: **John C. Hull, *Options, Futures, and
Other Derivatives*, 11th edition**. Chapter numbers below are for the 11th ed.;
the 10th ed. is within a chapter or two if that is what you have. Read the Hull
section for a topic before you implement it, do the comprehension questions in
[`NOTES.md`](NOTES.md), then write the code.

Free supplements:
- **Wikipedia** has solid derivations for this material.
- **QuantStart** has practical Python articles on MC and implied vol.
- **MIT OCW** and **Ben Lambert** give lecture-style intuition for the SDE/GBM
  and no-arbitrage foundations.

General foundation (read once, up front):
- Hull Ch. 5 (forward/futures, no-arbitrage pricing) and Ch. 14 (Wiener
  processes, Ito's lemma).
- MIT OCW **18.S096 / 15.401 Finance Theory** lecture notes on no-arbitrage and
  risk-neutral valuation (search "MIT OCW risk neutral valuation").

---

## 1. Black-Scholes (`black_scholes.py`)

**Read before implementing**
- Hull Ch. 15, esp. **15.6** (the BSM PDE), **15.8** (the pricing formulas),
  **15.9** (risk-neutral valuation). Dividend extension: Hull **17.4**.
- Wikipedia: "Black-Scholes model", the *Interpretation* and *Formula* sections.
  Note how `N(d2)` is the risk-neutral exercise probability.
- Optional intuition: Ben Lambert's "Black-Scholes" YouTube playlist; MIT OCW
  15.401 option-pricing lecture.

**Answer in NOTES.md before coding**
1. What are the six assumptions of the BSM model, and which one is most violated
   in real markets?
2. In `C = S*N(d1) - K*e^(-rT)*N(d2)`, what does each of `N(d1)` and `N(d2)`
   represent? Why is `N(d2)` the probability the option is exercised?
3. What is risk-neutral valuation, and why can we discount the expected payoff at
   the risk-free rate instead of a risk-adjusted rate?

---

## 2. Greeks (`greeks.py`)

**Read before implementing**
- Hull **Ch. 19** "The Greek Letters": 19.4 (delta), 19.5 (theta), 19.6 (gamma),
  19.8 (vega), 19.9 (rho), and the summary table at the end.
- Wikipedia: "Greeks (finance)" tabulates every closed-form Greek; use it to
  cross-check your formulas (mind the per-unit vs per-1% conventions).

**Answer in NOTES.md before coding**
1. Delta is `dV/dS`; derive why call delta = `N(d1)` (differentiate the price and
   watch the `N(d1)`/`N(d2)` terms cancel). Why is put delta `N(d1) - 1`?
2. Why is gamma identical for a call and a put on the same underlying/strike/expiry?
3. Theta is usually negative for a long option. What is it compensating the
   holder's counterparty for, and when can a European put have positive theta?

---

## 3. Implied volatility (`implied_vol.py`)

**Read before implementing**
- Hull **15.11** "Implied Volatilities" and **Ch. 20** "Volatility Smiles" for
  why IV varies by strike.
- Wikipedia: "Implied volatility" and "Brent's method". Understand why Brent
  (bracketing + inverse quadratic interpolation) is robust where Newton can
  diverge.
- `scipy.optimize.brentq` documentation: signature, what it needs (a sign change
  across the bracket), what it returns.
- QuantStart: "Implied Volatility ... using ... Newton-Raphson" (read for the
  problem setup even though we use Brent).

**Answer in NOTES.md before coding**
1. Why does a Black-Scholes price have a unique implied volatility for a valid
   market price? (Hint: what is the sign of vega?)
2. What are the no-arbitrage bounds on a European call price, and what should the
   solver do when a quoted price falls outside them?
3. Why prefer Brent over Newton-Raphson here, even though Newton is faster when
   it works? When does Newton break for deep OTM options?

---

## 4. Binomial tree (`binomial.py`)

**Read before implementing**
- Hull **Ch. 13** "Binomial Trees" (one- and two-step trees, risk-neutral `p`)
  and **Ch. 21.1 to 21.5** "Basic Numerical Procedures" (multi-step CRR, backward
  induction, American exercise).
- Wikipedia: "Binomial options pricing model", the CRR `u, d, p` parameterisation
  and the backward-induction pseudocode.

**Answer in NOTES.md before coding**
1. Derive the risk-neutral up-probability `p = (a - d)/(u - d)`. Why must
   `0 < p < 1`, and what breaks it?
2. Why does the CRR tree price converge to Black-Scholes as steps grow? What is
   the order of the error?
3. Explain, with a no-arbitrage argument, why it is never optimal to exercise an
   American call on a non-dividend-paying stock early. So why does the American
   put differ?

---

## 5. Monte Carlo (`monte_carlo.py`)

**Read before implementing**
- Hull **21.6** "Monte Carlo Simulation" and **21.7** on variance reduction
  (antithetic variables specifically). GBM exact solution: Hull **14.7** /
  eq. 21.22.
- QuantStart: the "European Vanilla Option Pricing ... via Monte Carlo" article
  (ignore the C++; read the method and variance-reduction sections).
- Wikipedia: "Monte Carlo methods for option pricing" and "Antithetic variates".

**Answer in NOTES.md before coding**
1. Write the exact solution for `S_T` under GBM. Why can European options be
   simulated in a single step with no time discretisation?
2. How does the Monte Carlo standard error scale with the number of paths, and
   what does that imply about the cost of one extra decimal place of accuracy?
3. Why do antithetic variates reduce variance? For which payoffs does the trick
   help most, and could it ever increase variance?

---

## 6. Market data (`market_data.py`)

**Read before implementing**
- Nothing new to price here. Read the provided `market_data.py` end to end and
  the sample CSV in `data/`.
- Optional: Hull **20.1** on how option quotes are organised into a chain.

**Answer in NOTES.md before coding**
1. What columns does `load_options_chain` guarantee downstream code, and what
   does it derive (time to expiry) versus require?
2. What day-count convention does it use for time to expiry, and how would using
   trading days instead of calendar days change your IVs?

---

## 7. IV surface (`surface.py`)

**Read before implementing**
- Hull **Ch. 20** "Volatility Smiles": the smile/skew across strikes and the
  term structure across maturities that the surface visualises.
- `matplotlib` `mplot3d` tutorial, specifically `Axes3D.plot_surface` and building
  coordinate grids with `numpy.meshgrid`.

**Answer in NOTES.md before coding**
1. What is a volatility smile / skew, and what does its existence tell you about
   how far real markets are from the Black-Scholes lognormal assumption?
2. Why do we typically build the surface from OTM options (calls above the spot,
   puts below) rather than mixing ITM and OTM quotes?
3. If the market genuinely obeyed Black-Scholes, what would the surface look like?
   (This is what the flat-surface round-trip test checks.)
