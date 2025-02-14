import logging
import numpy as np
import yfinance as yf

def get_latest_price(symbol: str) -> float:
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        
        if hist.empty:
            logging.warning(f"No historical data found for symbol: {symbol}")
            return 0

        latest_price = hist['Close'].iloc[-1]
        if np.isnan(latest_price):
            logging.warning(f"Latest price for {symbol} is NaN.")
            return 0
        
        return round(latest_price, 2)
    except Exception as e:
        logging.exception(f"Error retrieving latest price for symbol {symbol}: {e}")
        return 0
