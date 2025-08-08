import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_greek_DTE(df, greek):
    strikes = df['strike'].unique()
    
    plt.figure(figsize=(10, 6))
    for strike in sorted(strikes):
        subset = df[df['strike'] == strike]
        # Assuming dte is in years, convert to days
        dte_days = subset['dte'] * 365  # convert years to days if needed
        
        plt.plot(dte_days, subset[greek], label=f'Strike {strike}')
    
    plt.title(f"{greek.capitalize()} vs DTE")
    plt.xlabel("Days Till Expiry")
    plt.ylabel(greek.capitalize())
    plt.xlim(0, 180)  # limit x-axis to 0-180 days
    plt.grid(True)
    plt.legend(title="Strike")
    plt.show()


def plot_greek_vs_strike(df, greek, spot):
    import matplotlib.pyplot as plt

    dtes = sorted(df['dte'].unique())

    plt.figure(figsize=(10, 6))
    for dte in dtes:
        subset = df[df['dte'] == dte].copy()

        # Filter out bad data
        subset = subset[
            (subset[greek].notnull()) &
            (subset['strike'].notnull()) 
        ]

        # Sort by strike so the line doesn't zigzag
        subset = subset.sort_values(by='strike')

        # Optional smoothing (rolling average)
        subset[greek] = subset[greek].rolling(window=3, min_periods=1).mean()

        if not subset.empty:
            plt.plot(subset['strike'], subset[greek], label=f'DTE  { round(365*dte,2)}')

    plt.title(f"{greek.capitalize()} vs Strike (by DTE)")
    plt.xlabel("Strike Price")
    plt.ylabel(greek.capitalize())
    plt.xlim(0.85 * spot, 1.15 * spot)
    plt.grid(True)
    plt.legend(title="Days to Expiry")
    plt.show()