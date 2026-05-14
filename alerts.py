import os
from loguru import logger
from database.connection import SessionLocal
from database.models import MarketData, Coin, Alert

def check_alerts():
    """
    Checks active alerts against recent market data.
    """
    logger.info("Checking for triggered alerts...")
    db = SessionLocal()
    try:
        active_alerts = db.query(Alert).filter(Alert.is_active == True).all()
        if not active_alerts:
            return

        # Fetch latest prices for relevant coins
        coin_ids = [a.coin_id for a in active_alerts]
        latest_data = db.query(MarketData.coin_id, MarketData.price_usd)\
                        .filter(MarketData.coin_id.in_(coin_ids))\
                        .order_by(MarketData.timestamp.desc())\
                        .limit(len(coin_ids))\
                        .all()
                        
        price_map = {row.coin_id: row.price_usd for row in latest_data}
        
        for alert in active_alerts:
            current_price = price_map.get(alert.coin_id)
            if not current_price:
                continue
                
            triggered = False
            if alert.condition == 'above' and current_price > alert.target_price:
                triggered = True
            elif alert.condition == 'below' and current_price < alert.target_price:
                triggered = True
                
            if triggered:
                logger.warning(f"ALERT TRIGGERED! {alert.coin_id} is {alert.condition} {alert.target_price}. Current: {current_price}. Email: {alert.email}")
                # In production, integrate SendGrid or AWS SES here
                
                # Mark as inactive to prevent spam
                alert.is_active = False
                db.commit()
                
    except Exception as e:
        logger.error(f"Failed to process alerts: {e}")
    finally:
        db.close()
