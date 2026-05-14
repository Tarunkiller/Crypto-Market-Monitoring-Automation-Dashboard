from etl.extract import extract_coingecko_market_data, extract_binance_ticker_data
from etl.transform import transform_coingecko_data, transform_binance_data
from etl.load import load_data_to_db
from database.connection import SessionLocal
from loguru import logger

def run_coingecko_pipeline():
    logger.info("Starting CoinGecko ETL Pipeline...")
    raw_data = extract_coingecko_market_data(per_page=250, pages=1) # Top 250
    df = transform_coingecko_data(raw_data)
    
    db = SessionLocal()
    try:
        load_data_to_db(df, db)
        logger.info("CoinGecko ETL Pipeline completed successfully.")
    except Exception as e:
        logger.error(f"CoinGecko Pipeline failed: {e}")
    finally:
        db.close()

def run_binance_pipeline():
    logger.info("Starting Binance ETL Pipeline...")
    raw_data = extract_binance_ticker_data()
    df = transform_binance_data(raw_data)
    
    db = SessionLocal()
    try:
        # Note: Binance data 'id' mapping would need adjustment to match CoinGecko IDs if joining data.
        # For simplicity, we just use the symbol (lowercase) as the ID for Binance if ID is missing.
        df['id'] = df['symbol'].str.lower()
        load_data_to_db(df, db)
        logger.info("Binance ETL Pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Binance Pipeline failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_coingecko_pipeline()
    # run_binance_pipeline()
