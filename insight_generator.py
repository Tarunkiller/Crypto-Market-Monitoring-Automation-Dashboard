import pandas as pd
from datetime import datetime
from database.connection import SessionLocal
from database.models import MarketData, Coin
from analytics.embeddings import embed_documents
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from loguru import logger

def generate_daily_insight():
    """
    Fetches the latest market data, feeds it to an LLM to generate a plain-English 
    business insight report, and stores the embedded report in ChromaDB.
    """
    db = SessionLocal()
    try:
        # Fetch latest data for top coins
        # In a real scenario, this would use more complex SQLAlchemy queries to get 24h delta.
        # For this prototype, we'll fetch the most recent data block.
        logger.info("Generating daily insights from database...")
        
        # Simple fetch of recent data
        recent_data = db.query(Coin.name, MarketData.price_usd, MarketData.price_change_24h, MarketData.total_volume)\
                        .join(MarketData, Coin.id == MarketData.coin_id)\
                        .order_by(MarketData.timestamp.desc())\
                        .limit(50)\
                        .all()
                        
        if not recent_data:
            logger.warning("No recent data found to generate insights.")
            return
            
        # Format data as text
        data_text = "\n".join([f"{row.name}: Price ${row.price_usd:.2f}, 24h Change {row.price_change_24h}%, Volume {row.total_volume}" for row in recent_data])

        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.2)
        
        prompt = PromptTemplate.from_template(
            "You are a Crypto Market Analyst. Based on the following recent market data snapshot, "
            "generate a concise, highly professional daily market summary report. Highlight top gainers, losers, "
            "and identify any potential anomalies or volume trends. Give actionable recommendations if appropriate.\n\n"
            "Data:\n{data}\n\n"
            "Report Format: Markdown"
        )
        
        report_chain = prompt | llm
        report_content = report_chain.invoke({"data": data_text}).content
        
        logger.info("Report generated successfully. Storing in Vector Database...")
        
        # Store in Vector DB
        metadata = {
            "type": "daily_summary",
            "date": datetime.utcnow().strftime("%Y-%m-%d")
        }
        
        embed_documents(texts=[report_content], metadatas=[metadata])
        
        logger.info("Insight successfully generated and embedded.")
        return report_content

    except Exception as e:
        logger.error(f"Failed to generate insights: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_daily_insight()
