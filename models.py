from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Coin(Base):
    __tablename__ = "coins"

    id = Column(String, primary_key=True, index=True) # e.g., 'bitcoin'
    symbol = Column(String, unique=True, index=True)   # e.g., 'btc'
    name = Column(String)                             # e.g., 'Bitcoin'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    market_data = relationship("MarketData", back_populates="coin", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="coin")


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, ForeignKey("coins.id"), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    price_usd = Column(Float, nullable=False)
    market_cap = Column(Float)
    total_volume = Column(Float)
    price_change_24h = Column(Float)
    
    # Relationships
    coin = relationship("Coin", back_populates="market_data")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, ForeignKey("coins.id"))
    email = Column(String, index=True)
    target_price = Column(Float)
    condition = Column(String) # 'above' or 'below'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    coin = relationship("Coin", back_populates="alerts")


class Watchlist(Base):
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    coin_id = Column(String, ForeignKey("coins.id"))
    added_at = Column(DateTime, default=datetime.utcnow)
