from functions import funcs as rsi
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

def main():
    # 5 most active stocks from yahoo finance
    # *********************************************
    # CAN CHANGE TO DIFFERENT TICKER SYMBOLS
    # *********************************************
    stocks = ['NVDA', 'NIO', 'TSLA', 'INND', 'INTC']

    # calculate the today's date and the date exactly 1 years in the past
    present_date = date.today()
    past_date = present_date - relativedelta(years=1)
    present_date = present_date.strftime('%Y-%m-%d')
    past_date = past_date.strftime('%Y-%m-%d')

    # call the functions on the data
    stock_data = rsi.download_data(stocks, past_date, present_date)
    signal_df = rsi.analyze_prices(stock_data)
    rsi.backtest(signal_df, stock_data)


if __name__ == "__main__":
    main()