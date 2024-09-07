import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

# download data function
def download_data(ticker_symbols, start_date,  end_date):
        data = {}
        for symbol in ticker_symbols:
                symbol_data = yf.download(symbol, start=start_date, end=end_date)
                data[symbol] = symbol_data['Close']
        symbol_prices = pd.DataFrame(data)
        return symbol_prices


# function to calculate rsi given a series of closing prices
def calculate_rsi(ticker_data):
    delta = ticker_data.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    # rolling window of 14 days is recommended
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    # rsi formula
    rsi = 100 - (100/(1 + (avg_gain/avg_loss)))
    return rsi


# function to analyze prices of a stock x closing price df
# calculates the rsi for each day of a stock's closing price
# iterates through and checks if the rsi crosses thresholds
# returns a df of signals and its details
def analyze_prices(df):
    # list to keep track of the signals i.e. when rsi crosses thresholds
    signals = []
    for ticker in df.columns:
        # calculate rsi for each stock's closing prices
        rsi = calculate_rsi(df[ticker])

        # thresholds
        buy_threshold=30 
        sell_threshold=70
        
        # iterate through each day to check for signals
        for i in range(1, len(rsi)):
            previous_rsi = rsi.iloc[i - 1]
            current_rsi = rsi.iloc[i]
            date = rsi.index[i]

            # check if rsi crossees thresholds
            if previous_rsi >= buy_threshold and current_rsi < buy_threshold:
                signal = "Buy"
                signals.append([date, ticker, signal, current_rsi])
            elif previous_rsi <= sell_threshold and current_rsi > sell_threshold:
                signal = "Sell"
                signals.append([date, ticker, signal, current_rsi])

    # convert the list of signals into a df
    signals_df = pd.DataFrame(signals, columns=["Date", "Ticker", "Signal", "RSI"])

    return signals_df


# a function that backtests the strategy of using RSI signals to buy and sell stocks
# 
# buys a stock at first buy signal and sells at the first sell signal after
# sell signals after the first one are ignored until a new buy signal is triggered
# 
# if there is no buy signal for a stock, sell signals are ignored
# 
# outputs are printed to a text file
def backtest(signals_df, stock_prices_df):
    # sorts signals chronologically for the backtest
    signals_df = signals_df.sort_values(by="Date").reset_index(drop=True)

    # track transactions
    # trades consist of ticker and its details
    trades = {}
    total_profit = 0
    output_file = "results.txt"

    # open output file
    with open(output_file, "w") as file:
        # header
        file.write("Trading Strategy Results\n")
        file.write("************************\n\n")        
        
        # iterate through the rows of signals
        for i, row in signals_df.iterrows():
            date = row['Date']
            ticker = row['Ticker']
            signal = row['Signal']

            # get closing price
            closing_price = stock_prices_df.loc[date, ticker]

            # initialize ticker if not in trades
            if ticker not in trades:
                trades[ticker] = {'buy_price': None, 'buy_date': None, 'shares_bought': 0, 'sell_price': None, 'sell_date': None}

            # buy
            if signal == "Buy":
                if trades[ticker]['buy_price'] is None:
                    trades[ticker]['buy_price'] = closing_price
                    trades[ticker]['buy_date'] = date
                    trades[ticker]['shares_bought'] = 1000
                    result = f"Buy signal for {ticker} on {date.strftime('%Y-%m-%d')}: Bought {trades[ticker]['shares_bought']} shares at ${trades[ticker]['buy_price']:.2f}\n"
                    file.write(result)
            
            # sell
            elif signal == "Sell" and trades[ticker]['buy_price'] is not None:
                trades[ticker]['sell_price'] = closing_price
                trades[ticker]['sell_date'] = date
                profit = (trades[ticker]['sell_price'] - trades[ticker]['buy_price']) * trades[ticker]['shares_bought']
                total_profit += profit
                result = (f"Sell signal for {ticker} on {date.strftime('%Y-%m-%d')}: Sold {trades[ticker]['shares_bought']} shares at ${trades[ticker]['sell_price']:.2f}\n"
                          f"Profit from the trade: ${profit:.2f}\n")
                file.write(result) 
                # reset buy_price after selling so that we can buy and sell again accordingly
                trades[ticker]['buy_price'] = None
        
        # if no sell signals
        for ticker in trades:
            if trades[ticker]['buy_price'] is not None:
                result = f"No sell signal found for {ticker} after the last buy signal.\n"
                file.write(result)
        
        # if no buy signals
        if signals_df['Signal'].str.contains('Buy').sum() == 0:
            result = "No buy signals available.\n"
            file.write(result)


        # total profit
        result = f"\nTotal Profit: ${total_profit:.2f}\n"
        file.write(result) 
