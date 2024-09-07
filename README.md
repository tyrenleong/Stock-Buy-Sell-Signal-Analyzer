# Stock Buy/Sell Signal Analyzer


## Description
This project aims to analyze stocks for buy or sell signals using the Relative Strength Index (RSI). Generally, an RSI above 70 is considered overbought and an RSI below 30 is considered oversold. This analyzer will signal BUY when RSI <= 30 and SELL when RSI >= 70.
This will be backtested on a pre-defined list of stocks. When BUY signal is triggered, 1000 shares of a stock is bought. When SELL, 1000 shares will be sold if the stock was bought before. Details, profits, and total profits are written to a txt file.


## Installation

Clone the Repository


```bash
git clone https://github.com/tyrenleong/Stock-Buy-Sell-Signal-Analyzer.git
cd 
```

## Usage

To run:
```bash
python main.py
```
Please change the ticker symbols in main to change the symbols used in the backtest.
