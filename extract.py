from api.coingecko import CoinGeckoClient
from api.binance import BinanceClient
from loguru import logger

def extract_coingecko_market_data(per_page=100, pages=1):
    """
    Extracts market data for top coins from CoinGecko.
    """
    client = CoinGeckoClient()
    all_data = []
    
    logger.info(f"Extracting CoinGecko market data for {per_page * pages} coins...")
    for page in range(1, pages + 1):
        try:
            data = client.fetch_market_data(per_page=per_page, page=page)
            all_data.extend(data)
        except Exception as e:
            logger.error(f"Failed to fetch page {page} from CoinGecko: {e}")
            
    return all_data

def extract_binance_ticker_data():
    """
    Extracts 24h ticker data for all trading pairs on Binance.
    """
    client = BinanceClient()
    logger.info("Extracting Binance 24h ticker data...")
    try:
        data = client.fetch_ticker_24h()
        return data
    except Exception as e:
        logger.error(f"Failed to fetch from Binance: {e}")
        return []
