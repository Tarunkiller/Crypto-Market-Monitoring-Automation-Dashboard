import pandas as pd
from loguru import logger

def transform_coingecko_data(raw_data):
    """
    Cleans and transforms raw CoinGecko market data.
    """
    if not raw_data:
        logger.warning("No data to transform.")
        return pd.DataFrame()
        
    df = pd.DataFrame(raw_data)
    
    # Select necessary columns
    columns_to_keep = [
        'id', 'symbol', 'name', 'current_price', 'market_cap', 
        'total_volume', 'price_change_percentage_24h', 'last_updated'
    ]
    
    # Check which columns exist
    existing_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_cols]
    
    # Handle missing values
    df.fillna({'market_cap': 0, 'total_volume': 0, 'price_change_percentage_24h': 0.0}, inplace=True)
    
    # Standardize column names for the database
    df.rename(columns={
        'current_price': 'price_usd',
        'price_change_percentage_24h': 'price_change_24h',
        'last_updated': 'timestamp'
    }, inplace=True)
    
    # Convert timestamps to datetime if present
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
    # Remove duplicates
    df.drop_duplicates(subset=['id'], inplace=True)
    
    logger.info(f"Transformed {len(df)} records from CoinGecko data.")
    return df

def transform_binance_data(raw_data):
    """
    Cleans and transforms raw Binance ticker data.
    Focus on USDT pairs as a standard.
    """
    if not raw_data:
        return pd.DataFrame()
        
    df = pd.DataFrame(raw_data)
    
    # Filter for USDT pairs
    df = df[df['symbol'].str.endswith('USDT')]
    
    columns_to_keep = ['symbol', 'lastPrice', 'volume', 'priceChangePercent']
    existing_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_cols]
    
    # Convert data types
    numeric_cols = ['lastPrice', 'volume', 'priceChangePercent']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    df.rename(columns={
        'lastPrice': 'price_usd',
        'volume': 'total_volume',
        'priceChangePercent': 'price_change_24h'
    }, inplace=True)
    
    logger.info(f"Transformed {len(df)} records from Binance data.")
    return df
