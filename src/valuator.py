# import necessary libraries
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta

# Function to valuate trade 
def valuator(stock: str, end_date: str = None):
    # Use current date if end_date is not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    # if stock is not a valid ticker, return False
    if not yf.Ticker(stock).info:
        print('Invalid stock ticker. Try Again!')

    # Calculate valuated price using DCF method
    valuated_price = DCF(stock)
    if valuated_price is None:
        print('DCF calculation cannot be done.')

    # Download stock's adjusted close price
    try:
        current_price = yf.download(
            stock, start='2015-01-01', end=end_date)['Adj Close'].iloc[-1]
    except Exception as e:
        print(f"Failed to download stock data: {e}")
        return None  # Return None or some default value to handle this in the calling function


    # Truncate prices to the second decimal place
    truncated_current_price = np.trunc(current_price * 100) / 100
    truncated_valuated_price = np.trunc(valuated_price * 100) / 100

    # return a dictionary with the current price, valuated price, and valuation
    if truncated_current_price > truncated_valuated_price:
        return {"current_price": truncated_current_price, "valuated_price": truncated_valuated_price, "valuation": "overvalued"}
    elif truncated_current_price < truncated_valuated_price:
        return {"current_price": truncated_current_price, "valuated_price": truncated_valuated_price, "valuation": "undervalued"}
    else:
        return {"current_price": truncated_current_price, "valuated_price": truncated_valuated_price, "valuation": "fairly valued"}
      
