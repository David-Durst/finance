import yfinance as yf
#import yahoo_fin as yf
import pandas as pd
from currency_converter import CurrencyConverter

financial_keys = ['Total Revenue', 'Net Income', 'Basic EPS']
info_keys = ['currentPrice', 'trailingEps', 'forwardEps', 'revenueGrowth', 'targetMeanPrice',
             'targetMedianPrice', 'targetLowPrice', 'targetHighPrice', 'numberOfAnalystOpinions']
rename_cols = {
    'Total Revenue': 'Total Revenue ($B)',
    'Net Income': 'Net Income ($B)',
    'Basic EPS': 'EPS - Trailing, FY',
    'currentPrice': 'Current Price ($)',
    'trailingEps': 'EPS - Trailing, TTM',
    'forwardEps': 'EPS - Forward, TTM',
    'revenueGrowth': 'Revenue Growth',
    'targetMeanPrice': 'Target Mean Price ($)',
    'targetMedianPrice': 'Target Median Price ($)',
    'targetLowPrice': 'Target Low Price ($)',
    'targetHighPrice': 'Target High Price ($)',
    'numberOfAnalystOpinions': 'Number of Analyst Opinions'
}
c = CurrencyConverter()

def analyze_one_stock(ticker='MU'):
    stock = yf.Ticker(ticker)

    stock_info = stock.info
    if 'trailingEps' not in stock_info:
        # https://finance.yahoo.com/quote/000660.KS/financials/ (TTM EPS)
        stock_info['trailingEps'] = -6710
        # https://finance.yahoo.com/quote/000660.KS/analysis/ (EPS Trend next year)
        stock_info['forwardEps'] = 23309.1
    info_series = pd.Series(stock.info).loc[info_keys]
    financials_series = stock.financials.loc[financial_keys, :].iloc[:, 0].copy()
    if ticker == '000660.KS':
        for k in info_keys:
            if 'Analyst' in k:
                continue
            info_series[k] = c.convert(info_series[k], 'KRW', 'USD')
        for k in financial_keys:
            financials_series[k] = c.convert(financials_series[k], 'KRW', 'USD')

    financials_series['Net Margin'] = financials_series['Net Income'] / financials_series['Total Revenue'] * 100
    #financials_series['End of Period'] = stock.financials.iloc[0].index[0]

    stock_series = pd.concat([financials_series, info_series])
    stock_series['P/E'] = stock_series['currentPrice'] / (stock_series['trailingEps'] if stock_series['trailingEps'] != 0 else 0.000001)
    stock_series['Forward P/E'] = stock_series['currentPrice'] / (stock_series['forwardEps'] if stock_series['forwardEps'] != 0 else 0.000001)
    stock_series['Total Revenue'] /= 1e9
    stock_series['Net Income'] /= 1e9
    stock_series.name = stock.info['shortName']
    stock_series.rename(rename_cols, inplace=True)
    return stock_series


reorder_columns = [
    "Current Price ($)",
    "Target Mean Price ($)",
    "Target Median Price ($)",
    "Target Low Price ($)",
    "Target High Price ($)",
    "Total Revenue ($B)",
    "Net Income ($B)",
    'P/E',
    'Forward P/E',
    "EPS - Trailing, FY",
    "EPS - Trailing, TTM",
    "EPS - Forward, TTM",
    "Net Margin",
    "Revenue Growth",
    "Number of Analyst Opinions",
]


def analyze_all_stocks():
    stocks = []
    for ticker in ['NVDA', 'MSFT', 'AMZN', 'MU', '000660.KS', 'GFS', 'TSEM', 'AVGO', 'DELL', 'HPE']:
        print(ticker)
        stocks.append(analyze_one_stock(ticker))
    stocks_df = pd.concat(stocks, axis=1)
    stocks_df = stocks_df.loc[reorder_columns]
    stocks_df.to_excel('ai_analysis.xlsx')

if __name__ == '__main__':
    analyze_all_stocks()
