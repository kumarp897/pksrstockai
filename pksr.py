import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(symbol, period="30d", interval="1d"):
    """
    Download stock data from Yahoo Finance
    """
    data = yf.download(symbol, period=period, interval=interval)
    return data

def calculate_rsi(data, window=14):
    """
    Calculate Relative Strength Index (RSI)
    """
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def calculate_ma(data, window=10):
    """
    Calculate Moving Average
    """
    data[f"MA_{window}"] = data['Close'].rolling(window=window).mean()
    return data

def generate_signal(data):
    """
    Generate Bullish or Bearish Signal
    """
    today = data.iloc[-1]
    if today['Close'] > today['MA_10'] and today['RSI'] < 70:
        return "Bullish"
    elif today['Close'] < today['MA_10'] or today['RSI'] > 70:
        return "Bearish"
    else:
        return "Neutral"

def main():
    symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    data = get_stock_data(symbol)
    data = calculate_ma(data)
    data = calculate_rsi(data)
    signal = generate_signal(data)
    
    print(f"\nStock: {symbol}")
    print(f"Today's Close: {data['Close'][-1]:.2f}")
    print(f"10-day MA: {data['MA_10'][-1]:.2f}")
    print(f"RSI: {data['RSI'][-1]:.2f}")
    print(f"Signal: {signal}")

if __name__ == "__main__":
    main()