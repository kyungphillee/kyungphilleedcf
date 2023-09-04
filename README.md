# DCF-based Trading Bot

## Overview
This trading bot is a Python-based application that aims to help investors and traders in the stock market. It performs three major functions:

1. **Stock Selection**: The bot identifies the top 5 stocks based on volatility from the S&P 500.
2. **Stock Valuation**: It values stocks using the Discounted Cash Flow (DCF) model.
3. **Portfolio Optimization**: It optimizes your stock portfolio based on tangency portfolio theory.
4. **Trade Execution**: It enters and exits trades based on valuation and optimization strategies.

## Requirements
- Python 3.x
- Pandas
- NumPy
- yfinance
- Matplotlib (Optional for visualizations)
- Seaborn (Optional for visualizations)

## Installation
```bash
pip install pandas numpy yfinance matplotlib seaborn
```

## How It Works
1. **Stock Selection**: The bot scrapes S&P 500 stock data from Wikipedia and uses Yahoo Finance to determine their volatility.

2. **Stock Valuation (DCF Model)**:
    - It uses Yahoo Finance API to fetch necessary financial statements and metrics.
    - Calculates the Discounted Cash Flow (DCF) to valuate stocks.
  
3. **Portfolio Optimization**:
    - Uses Tangency Portfolio optimization to determine the weight of each asset in the portfolio.
  
4. **Trade Execution**:
    - Enters and exits trades based on the valuation.
  
## Sample Code
To instantiate a trader with an initial capital of $10,000 and perform a trade:
```python
trader = Trader(10000)
trader.enter_trade()
```

## Code Quality
The code is written with readability, modularity, and efficiency in mind. It includes caching mechanisms to minimize API calls, thereby improving performance. It also includes robust error handling to deal with various edge cases like invalid tickers or failed API calls.

### Features
- **Global Cache**: Avoids redundant API calls by storing fetched data.
- **Modularity**: Functions are organized based on their purpose, which makes it easy to understand and modify the code.
- **Error Handling**: The bot gracefully handles unexpected situations such as data fetch errors.

### Limitations
- **Data Freshness**: The cache stores data for a single run. If the bot needs up-to-date data, you need to run it again.
- **Risk Management**: The current implementation doesn't include any risk management features. It is advisable to integrate this bot as part of a broader risk management strategy.

## Code Review Notes
- **Efficiency**: Cache usage is well-optimized, though a more advanced caching mechanism could be implemented for even better performance.
- **Vulnerability**: No code vulnerabilities were found. However, the application is dependent on third-party services like Yahoo Finance, so there might be limitations based on their API.
- **Testing**: Unit tests are not included in the current implementation.

## Contribution
Feel free to fork this project, open issues, or submit PRs. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

## Disclaimer
This bot is for informational purposes only. Always do your own due diligence before making any investment decisions.
