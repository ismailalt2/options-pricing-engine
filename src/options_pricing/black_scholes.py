from __future__ import annotations
import numpy as np
from scipy.stats import norm


from .validation import (
    validate_nonnegative,
    validate_option_type,
    validate_positive,
)


def d1(S: float, K: float, r: float, sigma: float, T: float, q: float = 0.0):

    
    return  (np.log(S / K) + (r - q + sigma**2 / 2)*T) / (sigma*np.sqrt(T))




def d2(S: float, K: float, r: float, sigma: float, T: float, q: float = 0.0) -> float:  
    return (np.log(S/K) + (r-q- sigma**2/2)*T) / (sigma*np.sqrt(T))



def black_scholes_price(S: float,K: float,r: float,sigma: float,T: float,option_type: str,q: float = 0.0,) -> float:
    
    validate_positive("S", S)
    validate_positive("K", K)
    validate_positive("sigma", sigma)
    validate_positive("T", T)
    validate_nonnegative("q", q)
    option_type = validate_option_type(option_type)

    D1 = d1(S, K, r, sigma, T, q)
    D2 = d2(S, K, r, sigma, T, q)

    if option_type == "call":
        return S*np.exp(-q*T)*norm.cdf(D1) - K * np.exp(-r*T)*norm.cdf(D2) # call 
    else:
        return K * np.exp(-r*T)*norm.cdf(-D2) - S*np.exp(-q*T)*norm.cdf(-D1) # put