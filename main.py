import data as dt
from greeks import Greeks
import yfinance as yf
import pandas as pd
import plots as plot

class OptionAnalysis:
    def __init__(self, ticker):
        self.ticker = ticker
        self.spot = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
        self.r = dt.risk_free_rate()
        self.options = dt.options_chain(ticker)
        self.greeks_df = None

    def calculate_greeks(self):
        results = []
        for _, row in self.options.iterrows():
            iv = row['impliedVolatility']
            strike = row['strike']
            dte = row['dte']
            if pd.isna(iv) or iv <= 0 or strike <= 0 or dte <= 0 or self.spot <= 0:
                continue

            g = Greeks(S=self.spot, T=dte, K=strike, r=self.r, sigma=iv)
            primary = g.primary_greeks('call' if row['Call'] else 'put')
            secondary = g.secondary_greeks()
            greek_vals = {**primary, **secondary}

            greek_vals.update({
                'strike': strike,
                'dte': dte,
                'Call': row['Call'],
                'iv': iv
            })
            results.append(greek_vals)

        self.greeks_df = pd.DataFrame(results)
        print('Current spot price is %f' % self.spot)
        return self.greeks_df 
    
    def closest_strike(self, num_strikes=5):
        strikes = self.options['strike'].unique()
        differences = {}

        for strike in strikes:
            differences[strike] = abs(strike - self.spot)

        closest = sorted(differences, key=differences.get)[:num_strikes]

        filtered_df_calls = self.greeks_df[
           (self.greeks_df['strike'].isin(closest)) & (self.greeks_df['Call'] == True)
           ].copy()
        
        filtered_df_puts = self.greeks_df[
           (self.greeks_df['strike'].isin(closest)) & (self.greeks_df['Call'] == False)
           ].copy()
        
        return filtered_df_calls.sort_values(by=['strike', 'dte']), filtered_df_puts.sort_values(by=['strike', 'dte'])
    
if __name__ == "__main__":
    analysis = OptionAnalysis("SPY")
    df = analysis.calculate_greeks()
    print(df.head())
    calls_df, puts_df = analysis.closest_strike(5)
    greek_columns = df.columns[:8]

    for greek in greek_columns:
        plot.plot_greek(calls_df,greek)
        plot.plot_greek(puts_df,greek)
    
