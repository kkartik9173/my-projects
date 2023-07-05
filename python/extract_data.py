import yfinance as yf

# Define the ticker symbol as per Yahoo's format.
tickerSymbol = 'EURUSD=X'

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2000-1-1', end='2020-5-12')

# See your data
print(type(tickerDf))

import pandas as pd

def calculate_rsi(df, column="Close", period=14):
    # Get the difference in price from the previous step
    delta = df[column].diff().dropna()
    
    # Make two series: one for lower closes and one for higher closes
    up = delta.copy()
    up[up < 0] = 0
    down = -1 * delta.copy()
    down[down < 0] = 0
    
    # Calculate the EWMA (Exponential Weighted Moving Average)
    average_gain = up.ewm(com=(period - 1), min_periods=period).mean()
    average_loss = down.ewm(com=(period - 1), min_periods=period).mean()
    
    # Calculate the RS (Relative Strength)
    relative_strength = average_gain / average_loss
    
    # Calculate the RSI (Relative Strength Index)
    rsi = 100 - (100 / (1 + relative_strength))
    
    df['RSI'] = rsi

    return df

# Assuming you have your data in a DataFrame called df
df_with_rsi = calculate_rsi(tickerDf, column="Close", period=14)

def signal_based_on_rsi(df, rsi_column="RSI", upper=70, lower=30):
    df['Signal'] = 'Hold'
    df.loc[df[rsi_column] > upper, 'Signal'] = 'Sell'
    df.loc[df[rsi_column] < lower, 'Signal'] = 'Buy'
    print(df)
    return df

df_with_signals = signal_based_on_rsi(df_with_rsi, rsi_column="RSI", upper=70, lower=30)

# print(df_with_signals[df_with_signals["Signal"] != "Hold"])


df_with_signals.to_csv("./data.csv", header=True, index=True)

