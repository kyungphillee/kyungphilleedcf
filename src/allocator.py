import numpy as np
import pandas as pd
import yfinance as yf

# Tangency Portfolio
def tangency_portfolio(data):
   # calculates mean/expected return of each asset in portfolio 
    mu = data.mean() 

    # inverse of covariance matrix of the asset returns
    sigma = np.linalg.inv(data.cov()) 

    # one vector with number equal to columns
    one_vector = np.ones(len(data.columns)) 

    # dot product of inv.cov matrix and excess return over dot product of sigma, mu, and one
    return sigma @ mu / (one_vector @ sigma @ mu) 

def allocator(tickers):
    try:
        if 'portfolio_data' in stock_data_cache:
            data = stock_data_cache['portfolio_data']
        else:
            data = yf.download(tickers, start="2015-01-01", end=datetime.now().strftime('%Y-%m-%d'))['Adj Close']
            stock_data_cache['portfolio_data'] = data

        weights = tangency_portfolio(data)
        
        return weights.tolist()
        
    except yf.YFinanceError as yf_err:
        print(f"Yahoo Finance Error for portfolio: {yf_err}")
    except ValueError as val_err:
        print(f"Value error in portfolio calculation: {val_err}")
    except Exception as e:
        print(f"An unknown error occurred in portfolio: {e}")
        
    return []
