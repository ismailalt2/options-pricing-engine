# Learning Journal

One section per module. Fill each in **before and while** you implement that
module — the comprehension questions come from [`RESOURCES.md`](RESOURCES.md).
Write in your own words: this journal is what you will actually rehearse before
interviews, and re-deriving a formula from your own notes is the test of whether
you understood it or just typed it.

For each module, complete the five prompts:
- **What I read** — the exact Hull sections / links, so you can find them again.
- **Key formula** — the formula(s), written out, with each symbol defined.
- **Derivation sketch (my own words)** — how you'd rebuild it from scratch at a
  whiteboard. Not a copy of the book.
- **What confused me** — the sticking point and how you resolved it. This is the
  most valuable part; keep it honest.
- **Interview questions I should be able to answer** — start from the RESOURCES
  questions, add any a friend/interviewer might ask, and write your answers.

---

## 1. Black-Scholes — `black_scholes.py`

**What I read**
>

**Key formula**
> Call: C = …
> Put:  P = …
> d1 = … , d2 = …

**Derivation sketch (my own words)**
>

**What confused me**
>

**Interview questions I should be able to answer**
> - What are the BSM assumptions, and which fails worst in practice?
> - What do N(d1) and N(d2) mean? Why is N(d2) the exercise probability?
> - What is risk-neutral valuation and why is it valid?
> - (add your own)

---

## 2. Greeks — `greeks.py`

**What I read**
>

**Key formula**
> delta_call = … , delta_put = …
> gamma = … , vega = … , theta = … , rho = …

**Derivation sketch (my own words)**
>

**What confused me**
> (e.g. per-unit vs per-1% vega; theta per year vs per day; the sign of theta)

**Interview questions I should be able to answer**
> - Derive call delta = N(d1).
> - Why is gamma the same for calls and puts?
> - When is theta positive? What does gamma tell a delta-hedger?
> - (add your own)

---

## 3. Implied volatility — `implied_vol.py`

**What I read**
>

**Key formula**
> Solve f(σ) = BS_price(σ) − market_price = 0 for σ.

**Derivation sketch (my own words)**
>

**What confused me**
> (e.g. why the root is unique; how wide the bracket must be; no-arb bounds)

**Interview questions I should be able to answer**
> - Why is implied vol unique for a valid price?
> - Brent vs Newton — trade-offs, and when Newton fails.
> - What are the no-arbitrage bounds on a call, and how do you handle a violation?
> - (add your own)

---

## 4. Binomial tree — `binomial.py`

**What I read**
>

**Key formula**
> u = e^{σ√Δt}, d = 1/u, a = e^{(r−q)Δt}, p = (a−d)/(u−d)
> node value = e^{−rΔt}(p·V_up + (1−p)·V_down); American: max(that, intrinsic)

**Derivation sketch (my own words)**
>

**What confused me**
> (e.g. why 0<p<1 can fail; backward induction indexing; American vs European)

**Interview questions I should be able to answer**
> - Derive the risk-neutral probability p.
> - Why does CRR converge to Black-Scholes, and at what rate?
> - Why never exercise an American call early (no dividends)? Why is the put different?
> - (add your own)

---

## 5. Monte Carlo — `monte_carlo.py`

**What I read**
>

**Key formula**
> S_T = S·exp((r−q−σ²/2)T + σ√T·Z), Z~N(0,1)
> price ≈ e^{−rT}·mean(payoff); std_error = e^{−rT}·std(payoff)/√n

**Derivation sketch (my own words)**
>

**What confused me**
> (e.g. why single-step is exact for European; antithetic pairing; se vs error)

**Interview questions I should be able to answer**
> - Why can European payoffs be simulated in one step?
> - How does standard error scale with n? Cost of another decimal place?
> - Why do antithetic variates cut variance, and when might they not?
> - (add your own)

---

## 6. Market data — `market_data.py`

**What I read**
>

**Key formula / schema**
> Required columns: … ; derived: time_to_expiry = (expiry − quote)/365.

**Derivation sketch (my own words)**
> (Trace what the loader does to one row.)

**What confused me**
>

**Interview questions I should be able to answer**
> - What does the loader guarantee downstream vs require as input?
> - Calendar-day vs trading-day time to expiry — effect on IV?
> - (add your own)

---

## 7. IV surface — `surface.py`

**What I read**
>

**Key formula / idea**
> For each quote: σ_impl = implied_volatility(price, S, K, r, T, type, q).
> Arrange σ_impl on a (strike, time_to_expiry) grid; plot in 3D.

**Derivation sketch (my own words)**
>

**What confused me**
> (e.g. pivoting into a grid; handling NaNs; why OTM options)

**Interview questions I should be able to answer**
> - What is a vol smile / skew and what does it imply about BSM?
> - Why build the surface from OTM options?
> - What would the surface look like if markets obeyed Black-Scholes?
> - (add your own)
