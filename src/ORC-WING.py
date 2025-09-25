import yfinance as yf
import math as math
from numpy import ndarray, array, arange, zeros, ones, argmin, minimum, maximum, clip
from numpy.linalg import norm
from numpy.random import normal
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from data import risk_free_rate, options_chain, moneyness_array
from greeks import Greeks



class OrcWingModel:
    @staticmethod
    def volskew(moneyness: ndarray, vc: float, sc: float, pc: float, cc: float, dc: float, uc: float, dsm: float,
                 usm: float) -> ndarray:
        
        """
        Calculating the volatility skew settings in the Orc Model.
            
        Parameters
        ----------
        moneyness : ndarray
            Array of converted strike/moneyness values. Moneyness is 
        vc : float
            The current volatility (vc) at central skew point (Ref is reference price).
            vc = vr - VCR * ssr * (F- Ref) / Ref. Range is 0.05%-400%
        sc : float
            The current slope (sc) at central skew point (Ref is reference price).
            sc = sr - SCR * ssr * (F- Ref) / Ref
        pc : float
            The put curvature (pc) is a skew setting that shows the amount of bending of the
            volatility curve on the put wing between down cutoff and central skew point.
        cc : float
            The call curvature (cc) is a skew setting that shows the amount of bending of the
            volatility curve on the call wing between central skew point and up cutoff.
        dc : float
            The down cutoff (du) is a skew setting that defines a transition point between the put
            wing and the down smoothing range. This point corresponds to X=F*exp(Dcut). Range is < 0
        uc : float
            The up cutoff (uc) is a skew setting that defines a transition point between the call wing
            and the up smoothing range. This point corresponds to X=F*exp(Ucut). Range is > 0
        dsm : float
            The down smoothing range (dsm) is a skew setting that defines a length of the range
            on the strike scale where the volatility curve gradually changes from down cutoff to
            constant volatility level. The length of this range is defined in relation to the length of
            the put wing. Default value is 0.5. Range is > 0
        usm : float
            The up smoothing range (usm) is a skew setting that defines a length of the range on
            the strike scale where the volatility curve gradually changes from up cutoff to constant
            volatility level. The length of this range is defined in relation to the length of the call
            wing. Default value is 0.5. Range is > 0
        
        ----------
        Returns:
        ----------
        Array: An array of calculated volatilities for the different strikes.

        """
        

        #Want to establish our parameter bounds
        assert 0 < uc < 1  # Upper Cutoff bounds 
        assert -1 < dc < 0 # Down Cutoff Bounds
        assert dsm > 0 #Down smoothing range
        assert usm > 0 #Upper smoothing range
        assert 1e-6 < vc < 4 #Current Volatility
        assert -1e6 < sc < 1e6 # This bound is important for the optimisation problem because without it the slope can blow up very quickly
        assert dc * (1+dsm) <= dc <= 0 <= uc <= uc * (1+usm) # This sets the bounds for each piecewise region in the curve

        volatilities = []
        for x in moneyness: 

            if dc < x <= 0:
                vol = vc + (sc*x) + (pc*x**2)

            elif 0 < x <= uc:
                vol = vc + (sc*x) + (cc*x**2)

            elif dc * (1 + dsm) < x <= dc:
                vol = vc - (1 + 1/dsm) * pc * dc**2 - (sc * dc) / (2*dsm) \
                    + (1 + 1/dsm)*(2*pc*dc + sc) * x - (pc/dsm + sc/(2*dc*dsm)) * x**2
                
            elif x < dc * (1 + dsm): 
                vol = vc + dc * (2 + dsm) * (sc/2) + (1 + dsm)*pc * dc**2

            elif  uc < x <= uc*(1 + usm):
                vol = vc - (1 + 1/usm)*cc* uc**2 - (sc*uc)/(2*usm) \
                    + (1 + 1/usm)*(2*cc*uc + sc)*x - (cc/usm + sc/(2*uc*usm))*x**2
                
            elif uc*(1+usm) < x:
                vol = vc + uc * (1 + usm) * (sc/2) + (1 + usm) * cc * uc**2

            else:
                raise ValueError(f"x = {x} is outside of valid moneyness ranges")
            
            volatilities.append(vol)
        return volatilities

    #@classmethod
    #def loss_function(cls, x: ndarray, iv: ndarray, vega: ndarray):
