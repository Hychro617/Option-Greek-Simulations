# Option-Greek-Simulations

This repository provides Python implementations for options pricing, calculation of option Greeks, 
and calibration of the ORC-Wing volatility model. It allows users to compute option prices, sensitivities, 
and fit market implied volatilities to the ORC-Wing model.

# Features
### Implemented:
- Utilities for fetching market options data and reference points
- Compute Black-Scholes option prices for calls and puts
- Calculate Greeks: Delta, Gamma, Vega, Theta, Rho, Vanna, Vomma, Charm
- Compute moneyness-based volatility skew using the ORC-Wing model 

### Work In Progress:
- Calibrate ORC-Wing parameters using market data (work in progress)
- Weighted loss function using vega for accurate ATM pricing (work in progress)
- Handle moneyness-based volatility skew (work in progress)
