import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_greek(df, greek):
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

