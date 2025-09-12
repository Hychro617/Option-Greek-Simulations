import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import data as dt

class Greeks:
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

    @property
    def pdf_d1(self):
        return norm.pdf(self.d1)
    
    def black_scholes(self):
        # Check if d2 and d1 have been calculated
        # Calculate Black Scholes Option Pricing for both calls and puts 
        call = self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        put = -self.S * norm.cdf(-self.d1) + self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)

        return call, put
        
    def delta(self, option_type='call'):
        """
        Calculate delta for call or put option.

        Args:
            option_type (str): 'call' or 'put'

        Returns:
            float: Delta value
        """
        if option_type.lower() == 'call':
            return norm.cdf(self.d1)
        elif option_type.lower() == 'put':
            return norm.cdf(self.d1) - 1
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def gamma(self):
        """
        Measures the rate of change of delta with respect to 
        changes in the underlying asset's price.

        Returns:
            float: Gamma
        """
        numerator = self.pdf_d1
        denominator = self.S * self.sigma * (self.T)**0.5
        gamma = numerator / denominator
        return gamma

    def vega(self):
        """
        Measures the sensitivity of the option's price to changes 
        in the volatility of the underlying asset.

        Returns:
            float: Vega
        """
        vega = self.S * self.pdf_d1 * (self.T)**0.5
        return vega

    def theta(self, option_type='call'):
        """
        Calculate theta (time decay) for call or put option (per day).
        
        Args:
            option_type (str): 'call' or 'put'

        Returns:
            float: Theta value per day
        """
        if option_type.lower() == 'call':
            theta = (-self.S * self.pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) \
                    - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        elif option_type.lower() == 'put':
            theta = (-self.S * self.pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) \
                    + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        
        return theta / 365


    def rho(self, option_type='call'):
        """
        Calculate rho (sensitivity to risk-free rate) for call or put option.

        Args:
            option_type (str): 'call' or 'put'

        Returns:
            float: Rho value
        """
        if option_type.lower() == 'call':
            rho_val = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        elif option_type.lower() == 'put':
            rho_val = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        return rho_val


    def vomma(self):
        """
        Measures the sensitivity of vega 
        to volatility changes.

        Returns:
            float: Vomma
        """
        vomma = self.vega() * (self.d1 * self.d2)/self.sigma
        return vomma

    def vanna(self):
        """
        Measures the sensitivity of delta to volatility
        or vega to the spot price

        Returns:
            float: vanna
        """
        vanna = -self.vega() * self.d2 / (self.sigma * self.S)
        return vanna
    
    def charm(self):
        """
        Measures the rate of change of delta with respect to time (delta decay)
        for both call and put options (identical in Black-Scholes).

        Returns:
            float: Charm value
        """
        charm_val = -self.pdf_d1 / (2 * np.sqrt(self.T)) * (
            (2 * self.r) / self.sigma - self.d2 * self.sigma)
        return charm_val


    def primary_greeks(self, option_type = 'call'):
        """
        Return the primary Greeks commonly used:
        Delta, Gamma, Vega, Theta, Rho
        """
        return {
            'delta': self.delta(option_type),
            'gamma': self.gamma(),
            'vega': self.vega(),
            'theta': self.theta(option_type),
            'rho': self.rho(option_type),
            }

    def secondary_greeks(self):
        """
        Return secondary or higher order Greeks:
        Vomma, Vanna, Charm
        """
        return {
            'vomma': self.vomma(),
            'vanna': self.vanna(),
            'charm': self.charm(),
        }
