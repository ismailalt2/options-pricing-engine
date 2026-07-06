
from __future__ import annotations
import numpy as np
from scipy.stats import norm
from .black_scholes import d1, d2


from .validation import (
    validate_nonnegative,
    validate_option_type,
    validate_positive,
)


def delta(S: float, K: float, r: float, sigma: float, T: float, option_type: str, q: float = 0.0):

    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    option_type = validate_option_type(option_type)

    D1 = d1(S, K, r, sigma, T, q)
    

    if option_type == "call":
        return np.exp(-q*T) * norm.cdf(D1)
    else:
        return np.exp(-q*T) * (norm.cdf(D1) - 1)

def gamma(S: float, K: float, r: float, sigma: float, T: float, q: float = 0.0):
    
    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    D1 = d1(S, K, r, sigma, T, q)

    return np.exp(-q*T) * norm.pdf(D1) / (S*sigma*np.sqrt(T))



def vega(S: float, K: float, r: float, sigma: float, T: float, q: float = 0.0):
    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    D1 = d1(S, K, r, sigma, T, q)

    return S * np.exp(-q*T) * norm.pdf(D1) * np.sqrt(T)



def theta(S: float, K: float, r: float, sigma: float, T: float, option_type: str, q: float = 0.0):

    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    option_type = validate_option_type(option_type)
    D1 = d1(S, K, r, sigma, T, q)
    D2 = d2(S, K, r, sigma, T, q)

    if option_type == "call":
        return - np.exp(-q*T) * S * norm.pdf(D1) * sigma / (2*np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(D2) + q * S * np.exp(-q*T) * norm.cdf(D1)
    else:
        return - np.exp(-q*T) * S * norm.pdf(D1) * sigma / (2*np.sqrt(T)) + r * K * np.exp(-r*T) * norm.cdf(-D2) - q * S * np.exp(-q*T) * norm.cdf(-D1)




def rho(S: float, K: float, r: float, sigma: float, T: float, option_type: str, q: float = 0.0):

    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    option_type = validate_option_type(option_type)
    D2 = d2(S, K, r, sigma, T, q)

    if option_type == "call":
        return K * T * np.exp(-r*T) * norm.cdf(D2)
    else:
        return -K * T * np.exp(-r*T) * norm.cdf(-D2)
