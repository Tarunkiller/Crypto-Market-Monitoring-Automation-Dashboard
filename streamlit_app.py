import streamlit as st
import pandas as pd
import requests
import os
from loguru import logger

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(page_title="Crypto Market Dashboard", layout="wide", page_icon="📈")

st.title("📈 Crypto Market Monitoring Dashboard")

# Fetch coins
@st.cache_data(ttl=300)
def fetch_coins():
    try:
        res = requests.get(f"{API_URL}/coins")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        logger.error(f"Failed to fetch coins: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_market_data(coin_id):
    try:
        res = requests.get(f"{API_URL}/market_data/{coin_id}")
        res.raise_for_status()
        return pd.DataFrame(res.json())
    except Exception as e:
        logger.error(f"Failed to fetch market data: {e}")
        return pd.DataFrame()

coins = fetch_coins()

if not coins:
    st.warning("No data available yet. Please ensure the backend and database are running and ETL pipelines have executed.")
else:
    # Sidebar
    st.sidebar.header("Controls")
    selected_coin = st.sidebar.selectbox("Select Coin", options=[c["id"] for c in coins])
    
    # Main content
    df = fetch_market_data(selected_coin)
    
    if df.empty:
        st.info("No historical data available for this coin.")
    else:
        # KPIs
        latest = df.iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price (USD)", f"${latest['price_usd']:.2f}", f"{latest.get('price_change_24h', 0.0)}%")
        col2.metric("Market Cap", f"${latest['market_cap']:,.0f}")
        col3.metric("Total Volume", f"${latest['total_volume']:,.0f}")
        
        # Charts
        st.subheader(f"Price History: {selected_coin.upper()}")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.line_chart(df.set_index('timestamp')['price_usd'])
