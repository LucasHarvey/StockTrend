# StockTrend

StockTrend is a project that uses fundamental data about companies (e.g. P/E ratio, D/E ratio, etc.) and machine learning to predict whether a company will outperform or underperform the S&P 500. 

- Data scraped from Yahoo! Finance from 2003-2013
- Data parsed into a pandas dataframe
- Linear SVM from sklearn trained to predict outperform/underperform based on fundamentals
- Backtesting over 2003-2013 and test set yielded approximately 17% returns compared to 7% from the market, beating the market by 10% over a 10-year period. 
- Data fetching from Quandl to obtain most recent market data and to make predictions on stocks likely to outperform the market by at least 5%
