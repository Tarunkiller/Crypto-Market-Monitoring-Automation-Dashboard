from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from database.connection import get_db
from database.models import Coin, MarketData
from analytics.rag_agent import RAGAnalyticsAgent
from loguru import logger

router = APIRouter()

# Global agent instance to maintain memory state (in production, use per-session memory)
agent_instance = None

def get_agent():
    global agent_instance
    if not agent_instance:
        agent_instance = RAGAnalyticsAgent()
    return agent_instance

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.get("/coins")
def get_coins(db: Session = Depends(get_db)):
    """Returns a list of all tracked coins."""
    coins = db.query(Coin).all()
    return [{"id": c.id, "symbol": c.symbol, "name": c.name} for c in coins]

@router.get("/market_data/{coin_id}")
def get_market_data(coin_id: str, limit: int = 100, db: Session = Depends(get_db)):
    """Returns historical market data for a specific coin."""
    data = db.query(MarketData)\
             .filter(MarketData.coin_id == coin_id)\
             .order_by(MarketData.timestamp.desc())\
             .limit(limit)\
             .all()
    if not data:
        raise HTTPException(status_code=404, detail="Coin not found or no data available")
    return data

@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest, agent: RAGAnalyticsAgent = Depends(get_agent)):
    """
    Interact with the RAG Copilot. 
    It will use PostgreSQL or Vector Store dynamically to answer the question.
    """
    logger.info(f"Received chat request: {request.message}")
    try:
        response = agent.chat(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing chat.")
