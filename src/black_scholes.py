import numpy as np
from scipy.stats import norm

class BlackScholes:

    def __init__(self, S, T, K, r, sigma):
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            raise ValueError("S, K, T, and sigma must be positive")
        self.S = S  # Price of spot
        self.T = T  # dte in years
        self.K = K  # Strike Price
        self.r = r  # Risk-free interest rate
        self.sigma = sigma # Annualised Volatility
        self._d1 = None
        self._d2 = None
    
    @property
    def d1(self):
        if self._d1 is None:
            self._d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return self._d1

    @property
    def d2(self):
        if self._d2 is None:
            self._d2 = self.d1 - self.sigma * np.sqrt(self.T)
        return self._d2

    def price(self):
        # Check if d2 and d1 have been calculated
        # Calculate Black Scholes Option Pricing for both calls and puts 
        call = self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        put = -self.S * norm.cdf(-self.d1) + self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)

        return call, put
    
"""

CHECKER
if __name__ == '__main__':
    S = 100   
    T = 0.8
    K = 105
    r = 0.03
    sigma = 0.3

    check = BlackScholes(S, T, K, r, sigma)
    call_price, put_price = check.price()
    print(f"The price of this hypothetical call is {call_price:.4f}")
    print(f"The price of this hypothetical put is {put_price:.4f}")
    
"""