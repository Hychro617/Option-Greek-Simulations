import pandas as pd
import yfinance as yf
import datetime
import math 



def options_chain(ticker: str) -> pd.DataFrame:
    data = yf.Ticker(ticker)
    expirations = data.options

    options_list = []

    for exp in expirations:
        option_chain = data.option_chain(exp)
        combined = pd.concat([option_chain.calls, option_chain.puts], ignore_index=True)
        combined['expirationDate'] = pd.to_datetime(exp)
        options_list.append(combined)

    options = pd.concat(options_list, ignore_index=True)

    # Days To Expiration (DTE) in years
    options['dte'] = (options['expirationDate'] - datetime.datetime.now()).dt.days / 365

    # True if call
    options['Call'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)

    # Ensure numeric columns
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)

    # Mid price
    options['mid'] = (options['bid'] + options['ask']) / 2

    # Drop unnecessary cols
    drop_cols = ['contractSize', 'currency', 'change', 'percentChange', 
                 'lastTradeDate', 'lastPrice']
    options = options.drop(columns=[col for col in drop_cols if col in options.columns])

    return options

def risk_free_rate():
    shy = yf.Ticker('SHY')
    # 'yield' is typically the dividend yield of the ETF as a decimal (e.g., 0.015 = 1.5%)
    rate = shy.info.get('yield', None)
    if rate is None:
        raise ValueError("Yield data not available from SHY ticker")
    return rate

def forward_price(ticker: str, T: float, q: float = 0.0) -> float:
    """
    Calculate forward price F = S * exp((r - q) * T)

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker symbol.
    T : float
        Time to expiration in years.
    q : float, optional
        Dividend yield, default is 0.

    Returns
    -------
    F : float
        Forward price
    """
    data = yf.Ticker(ticker)
    spot = data.history(period='1d')['Close'].iloc[-1]
    r = risk_free_rate()
    F = spot * math.exp((r - q) * T)
    return F


if __name__ == '__main__':
    ticker = "AAPL"

    # Get options data
    options = options_chain(ticker)

    # List available expirations
    expirations = options['expirationDate'].unique()
    print("Available expirations:")
    for i, exp in enumerate(expirations):
        print(f"{i}: {exp.date()}")

    # Ask user to pick an expiration by index
    while True:
        try:
            idx = int(input("Select expiration by index: "))
            selected_exp = expirations[idx]
            break
        except (IndexError, ValueError):
            print("Invalid index. Try again.")

    # Filter options for that expiration
    options_for_exp = options[options['expirationDate'] == selected_exp]

    # Get T (time to expiration) from any row in this expiration
    T = options_for_exp['dte'].iloc[0]

    # Calculate forward price
    F = forward_price(ticker, T)
    print(f"Forward price for expiration {selected_exp.date()}: {F:.2f}")
