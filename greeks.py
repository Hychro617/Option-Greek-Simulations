import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


class Greeks:
    def __init__(self, S, T, K, r, sigma):
        self.S = S  # Price of spot
        self.T = T  # dte in years
        self.K = K  # Strike Price
        self.r = r  # Risk-free interest rate
        self.sigma = sigma # Annualised Volatility
        self.d1 = None
        self.d2 = None

    def d_1(self):
        self.d1 = (np.log(self.S / self.K) + (self.r + (self.sigma**2)/2)* self.T)/ (self.sigma * np.sqrt(self.T))
        return self.d1
    
    def d_2(self):
        if self.d1 == None:
            self.d_1()
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)
        return self.d2
    
    def black_scholes(self):
        # Check if d2 and d1 have been calculated
        if self.d1 == None:
            self.d_1()
        if self.d2 == None:
            self.d_2()
        # Calculate Black Scholes Option Pricing for both calls and puts 
        call = self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        put = -self.S * norm.cdf(-self.d1) + self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)

        return call, put
    
    def call_delta(self):
        if self.d1 == None:
            self.d_1()
        # Measures the sensitivity of an option's price to changes in the spot price for a call option
        call_delta = norm.cdf(self.d1)
        return call_delta
    
    def put_delta(self):
        if self.d1 == None:
            self.d_1()
        # Measures the sensitivity of an option's price to changes in the spot price for a put option
        put_delta = norm.cdf(self.d1)-1
        return put_delta

    def gamma(self):
        if self.d1 == None:
            self.d_1()
        # Measures the rate of change of an option's delta 
        numerator = norm.pdf(self.d1)
        denominator = self.S * self.sigma * (self.T)**0.5
        gamma = numerator/denominator
        return gamma
    
    def vega(self):
        if self.d1 == None:
            self.d_1()
        # Measures the sensitivity of an option's price to volatility changes
        vega = self.S * norm.pdf(self.d1) * (self.T)**0.5
        return vega


