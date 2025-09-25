from analysis import OptionAnalysis
import plots as plot
from data import options_chain, forward_price, moneyness_array
import pandas as pd
import numpy as np
from greeks import Greeks


    
if __name__ == "__main__":
    ticker = "SPY"
    options = options_chain(ticker) # Get options data
    
    expirations = options['expirationDate'].unique() #List available expirations
    print("Available expirations:")
    for i, exp in enumerate(expirations):
        print(f"{i}: {exp.date()}")
    
    while True:
        try:
            idx = int(input("Select expiration by index: ")) # Ask user to pick an expiration by index
            selected_exp = expirations[idx]
            break
        except (IndexError, ValueError):
            print("Invalid index. Try again.")

    
    # Filter options for selected expiration
    options_for_exp = options[options['expirationDate'] == selected_exp]

    T = options_for_exp['dte'].iloc[0]
    F = forward_price(ticker, T)

    # Find the ATM strike row
    atm_strike_row = options_for_exp.iloc[(options_for_exp['strike'] - F).abs().argmin()]

    # Filter OTM and ATM options
    options_otm = options_for_exp[options_for_exp['inTheMoney'] == False].copy()
    options_for_moneyness = pd.concat([options_otm, pd.DataFrame([atm_strike_row])], ignore_index=True).drop_duplicates()

    # CALCULATE THE MONEYNESS ARRAY FOR ORC-WING
    Moneyness_array = moneyness_array(options_for_moneyness, F)
    Moneyness_array = np.sort(Moneyness_array)

    #CALCULATE THE VEGA ARRAY FOR ORC-WING LOSS FUNCTION
    for index, row in options_for_moneyness.iterrows():
        s = row['strike']
    print(options_for_moneyness)
        #Vega_array = Greeks.vega(contract)

    #print(Vega_array)

    
