# import necessary libraries
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta

# Pre-fetch treasury yield and market data
treasury_ticker = yf.Ticker('^TNX')
market_ticker = yf.Ticker('^GSPC')
risk_free_rate = treasury_ticker.history(period='max')['Close'].iloc[-1] / 100
market_history = market_ticker.history(period='max')['Close']


def fetch_stock_data(ticker):
    try:
        if ticker in stock_data_cache:
            return stock_data_cache[ticker]

        stock = yf.Ticker(ticker)
        info = stock.info
        financials = stock.financials
        income_statement = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow
        dividends = stock.dividends

        stock_data_cache[ticker] = (info, financials, income_statement, balance_sheet, cash_flow, dividends)
        
        return info, financials, income_statement, balance_sheet, cash_flow, dividends
    
    except yf.YFinanceError as yf_err:
        print(f"Yahoo Finance Error for {ticker}: {yf_err}")
    except Exception as e:
        print(f"An unknown error occurred for {ticker}: {e}")
        
    return None, None, None, None, None, None


# Function to calculate discount rate
def discount_rate(stock_data):
    info, financials, _, balance_sheet, _, _ = stock_data
    E = info['marketCap']
    D = balance_sheet.loc['Total Debt'].iloc[-1]
    V = E + D
    Tc = 0.21

    Interest_Expense = financials.loc['Interest Expense'].iloc[0]
    Rd = Interest_Expense / D * (1 - Tc)

    Re = cost_of_equity(stock_data)

    return (E/V) * Re + (D/V) * Rd * (1-Tc)

# Function to calculate cost of equity
def cost_of_equity(stock_data):
    info, _, _, _, _, _ = stock_data
    Beta = info['beta']

    last_date = market_history.index[-1]
    start_date = last_date - pd.DateOffset(years=5)
    filtered_data = market_history[start_date:last_date]
    daily_change = filtered_data.pct_change().dropna()
    annualized_return = ((1 + daily_change.mean()) ** 252 - 1)

    return risk_free_rate + Beta * (annualized_return - risk_free_rate)

# Function to get Free Cash Flow
def get_FCF(stock_data):
    _, financials, _, _, cash_flow, _ = stock_data
    CFO = cash_flow.loc['Operating Cash Flow'].iloc[0]
    IE = financials.loc['Interest Expense'].iloc[0]
    CAPEX = cash_flow.loc['Capital Expenditure'].iloc[0]
    return CFO + IE * (1 - 0.21) - CAPEX

# Function to calculate Terminal Value
def Terminal_Value(stock_data):
    info, _, income_statement, balance_sheet, _, dividends = stock_data
    FCFF = get_FCF(stock_data)
    dividend_paid = dividends.iloc[-1] if not dividends.empty else 0
    net_income = income_statement.loc['Net Income'].iloc[0]
    retention_rate = 1 - dividend_paid / net_income

    debt = balance_sheet.loc['Total Debt'].iloc[0]
    equity = info['marketCap']
    ROIC = (net_income - dividend_paid) / (debt + equity)

    g = retention_rate * ROIC
    r = discount_rate(stock_data)

    return FCFF * (1 + g) / (r - g)

# Main DCF function
def DCF(ticker, forecast_period=5):
    stock_data = fetch_stock_data(ticker)
    WACC = discount_rate(stock_data)
    FCFFn = get_FCF(stock_data)
    TV = Terminal_Value(stock_data)
    PV_TV = TV / (1 + WACC) ** forecast_period

    PV_FCFF = sum(FCFFn / (1 + WACC) **
                  i for i in range(1, forecast_period + 1))

    EV = PV_TV + PV_FCFF
    info = stock_data[0]
    Implied_Share_Price = EV / info['sharesOutstanding']
    return Implied_Share_Price
  
