
from scipy.stats import norm
from black_scholes import BlackScholes
import numpy as np
class Greeks(BlackScholes):

    @property
    def pdf_d1(self):
        return norm.pdf(self.d1)
    
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



"""
CHECKER

if __name__ == '__main__':
        # Example option parameters
    S = 100      # Spot price
    K = 105      # Strike price
    T = 0.5      # Time to expiration in years
    r = 0.03     # Risk-free rate
    sigma = 0.2  # Volatility

    # Black-Scholes price
    bs_option = BlackScholes(S, T, K, r, sigma)
    call_price, put_price = bs_option.price()
    print(f"Black-Scholes Prices:\nCall: {call_price:.4f}, Put: {put_price:.4f}\n")

    # Greeks calculations
    option = Greeks(S, T, K, r, sigma)

    print("Primary Greeks (Call):")
    for name, value in option.primary_greeks('call').items():
        print(f"{name.capitalize()}: {value:.6f}")

    print("\nPrimary Greeks (Put):")
    for name, value in option.primary_greeks('put').items():
        print(f"{name.capitalize()}: {value:.6f}")

    print("\nSecondary Greeks:")
    for name, value in option.secondary_greeks().items():
        print(f"{name.capitalize()}: {value:.6f}")

"""