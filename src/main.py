# import necessary libraries
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import allocator
import dcf_module 
import valuator

# Trade Executor
class Trader:
    def __init__(self, initial_capital=10000):
        self.portfolio = {}
        self.portfolio_value = 0
        self.initial_capital = initial_capital

    def enter_trade(self, tickers=None, end_date=None):
        # Use current date if end_date is not provided
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        if tickers is None:
            tickers = sp500_stocks()

        # if length of tickers is greater than 5, cut it down to the first five
        if len(tickers) > 5:
            tickers = tickers[:5]

        # Get list of weights
        weights = allocator(tickers)
        
        # Get valuation of each stock
        valuation = [valuator(ticker, end_date) for ticker in tickers]

        # set portfolio value to initial capital
        self.portfolio_value = self.initial_capital
        
        # Execute initial trades based on valuation

        for i in range(len(tickers)):
            value = valuation[i]['valuation']
            current_price = valuation[i]['current_price']

            num_shares = (weights[i] * self.initial_capital) / current_price

            if value == 'overvalued':
                self.portfolio[tickers[i]] = {'shares': -num_shares, 'total_value': -num_shares * current_price}
            elif value == 'undervalued':
                self.portfolio[tickers[i]] = {'shares': num_shares, 'total_value': num_shares * current_price}
            else:
                continue
            
        self.portfolio = pd.DataFrame(self.portfolio)
        return self.portfolio

    def exit_trade(self, tickers, end_date=None):
        # Use current date if end_date is not provided
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        # Get valuation of each stock
        valuation = [valuator(ticker, end_date) for ticker in tickers]

        # Get list of weights
        weights = allocator(tickers)

        # Check for exit condition
        for i in range(len(tickers)):
            value = valuation[i]['valuation']
            current_price = valuation[i]['current_price']

            # Calculate 0.5 standard deviation criteria for exiting trade
            if self.portfolio.get(tickers[i], 0) != 0:
                half_std = 0.5 * np.std(valuation[i]['current_price']) # Replace with appropriate std calculation if needed

                # Check if the exit condition is met and execute trade
                if value == 'overvalued' and valuation[i]['valuated_price'] <= current_price - half_std:
                    self.portfolio[tickers[i]]['total_value'] += current_price * weights[i]
                    self.portfolio[tickers[i]]['shares'] = self.portfolio[tickers[i]]['total_value'] / current_price
                    break
                elif value == 'undervalued' and valuation[i]['valuated_price'] >= current_price + half_std:
                    self.portfolio[tickers[i]]['total_value'] -= current_price * weights[i]
                    self.portfolio[tickers[i]]['shares'] = self.portfolio[tickers[i]]['total_value'] / current_price
                    break
                
        self.portfolio = pd.DataFrame(self.portfolio)
        return self.portfolio
    
    def calculate_portfolio_value(self, tickers, valuation):
        for i in range(len(tickers)):
            value = valuation[i]['valuation']
            if value == 'overvalued':
                self.portfolio_value -= self.portfolio[tickers[i]]['total_value']
            elif value == 'undervalued':
                self.portfolio_value += self.portfolio[tickers[i]]['total_value']

        return self.portfolio_value
