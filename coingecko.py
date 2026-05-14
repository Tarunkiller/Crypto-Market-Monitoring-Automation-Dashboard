import requests
import os
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.api_key = os.getenv("COINGECKO_API_KEY")
        self.headers = {"accept": "application/json"}
        if self.api_key:
            self.headers["x-cg-demo-api-key"] = self.api_key

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_market_data(self, vs_currency="usd", per_page=100, page=1):
        """
        Fetches live crypto prices, market cap, and volume from CoinGecko.
        """
        url = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False
        }
        
        logger.info(f"Fetching data from CoinGecko: {url}")
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 429:
            logger.warning("CoinGecko API rate limit reached, retrying...")
            response.raise_for_status()
            
        response.raise_for_status()
        return response.json()
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
    def fetch_historical_data(self, coin_id, vs_currency="usd", days=30):
        url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": vs_currency,
            "days": days
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
