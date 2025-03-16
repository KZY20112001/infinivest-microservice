import logging
import datetime
import numpy as np
import yfinance as yf
import requests

from app.openai_client import generate_asset_description

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


def get_asset_description(symbol: str) -> str:
    try:
        return generate_asset_description(symbol)
    except Exception as e:
        logging.exception(f"Error retrieving description for symbol {symbol}: {e}")
        return ""
    
    
def get_price_history(symbol: str) -> list[dict[str, float]]:
    try:
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=90)  # 3 months

        asset = yf.Ticker(symbol)
        data = asset.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        price_history = [
            {"date": str(index.date()), "close": round(row["Close"], 2)}
            for index, row in data.iterrows()
            ]
        return price_history

    except Exception as e:
        return {"error": f"Failed to retrieve price history for {symbol}: {str(e)}"}    
    
    

def get_assets(key_word: str) -> list[tuple[str, str]]:
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={key_word}&quotesCount=10&newsCount=0"
    headers = {
        "User-Agent": "Mozilla/5.0",  # Mimics a browser request
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        return [(quote["symbol"], quote.get("longname", "N/A")) for quote in data.get("quotes", []) if "symbol" in quote]
    except Exception as e:
        print(f"Error fetching assets: {e}")
        return []