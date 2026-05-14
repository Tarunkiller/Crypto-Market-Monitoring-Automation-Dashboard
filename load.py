from sqlalchemy.orm import Session
from database.models import Coin, MarketData
from loguru import logger
import pandas as pd
from datetime import datetime

def load_data_to_db(df: pd.DataFrame, db: Session):
    """
    Loads the transformed dataframe into the PostgreSQL database.
    Ensures Coin records exist, then inserts MarketData.
    """
    if df.empty:
        logger.warning("Dataframe is empty, nothing to load.")
        return

    try:
        # Load Coins
        existing_coins = {coin.id for coin in db.query(Coin.id).all()}
        
        new_coins = []
        for _, row in df.iterrows():
            coin_id = row.get('id', row.get('symbol', '').lower())
            symbol = row.get('symbol', '').lower()
            name = row.get('name', symbol.upper())
            
            if coin_id not in existing_coins:
                new_coins.append(Coin(id=coin_id, symbol=symbol, name=name))
                existing_coins.add(coin_id)
                
        if new_coins:
            db.add_all(new_coins)
            db.commit()
            logger.info(f"Inserted {len(new_coins)} new coins.")
            
        # Load Market Data
        market_data_records = []
        for _, row in df.iterrows():
            coin_id = row.get('id', row.get('symbol', '').lower())
            record = MarketData(
                coin_id=coin_id,
                timestamp=row.get('timestamp', datetime.utcnow()),
                price_usd=row.get('price_usd', 0.0),
                market_cap=row.get('market_cap', 0.0),
                total_volume=row.get('total_volume', 0.0),
                price_change_24h=row.get('price_change_24h', 0.0)
            )
            market_data_records.append(record)
            
        if market_data_records:
            # Batch insert
            db.bulk_save_objects(market_data_records)
            db.commit()
            logger.info(f"Loaded {len(market_data_records)} market data records.")
            
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading data to DB: {e}")
        raise
