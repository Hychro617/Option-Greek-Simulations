import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from greeks import Greeks


def options_chain(ticker):
    data = yf.Ticker(ticker)
    expirations = data.options
    
    options_list = []  # List to collect DataFrames
    
    for exp in expirations:
        option_chain = data.option_chain(exp)
        combined = pd.concat([option_chain.calls, option_chain.puts], ignore_index=True)
        combined['expirationDate'] = pd.to_datetime(exp)
        options_list.append(combined)
    
    options = pd.concat(options_list, ignore_index=True)

    # Add Days To Expiration (DTE) in years
    options['dte'] = (options['expirationDate'] - datetime.datetime.now()).dt.days / 365

    # True if a call option
    options['Call'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)

    # Ensure numeric columns are correct dtype
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)

    # Mid price
    options['mid'] = (options['bid'] + options['ask']) / 2

    # Drop unnecessary columns
    drop_cols = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice']
    options = options.drop(columns=[col for col in drop_cols if col in options.columns])

    return options

def risk_free_rate():
    shy = yf.Ticker('SHY')
    # 'yield' is typically the dividend yield of the ETF as a decimal (e.g., 0.015 = 1.5%)
    rate = shy.info.get('yield', None)
    if rate is None:
        raise ValueError("Yield data not available from SHY ticker")
    return rate

