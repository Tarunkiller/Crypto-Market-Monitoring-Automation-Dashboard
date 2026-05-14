import requests
import os
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class BinanceClient:
    BASE_URL = "https://api.binance.com/api/v3"

    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers["X-MBX-APIKEY"] = self.api_key

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
    def fetch_ticker_24h(self, symbol=None):
        """
        24 hour rolling window price change statistics.
        If symbol is provided, fetches for single symbol, else for all symbols.
        """
        url = f"{self.BASE_URL}/ticker/24hr"
        params = {}
        if symbol:
            params["symbol"] = symbol

        logger.info(f"Fetching 24hr ticker from Binance for symbol: {symbol or 'ALL'}")
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
    def fetch_klines(self, symbol, interval="1d", limit=30):
        """
        Kline/candlestick bars for a symbol.
        """
        url = f"{self.BASE_URL}/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
