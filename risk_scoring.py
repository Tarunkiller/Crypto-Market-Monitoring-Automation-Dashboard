import pandas as pd
import numpy as np

def calculate_risk_score(df: pd.DataFrame):
    """
    Calculates a simple risk score for a coin based on volatility.
    High volatility -> High risk.
    """
    if df.empty or len(df) < 5:
        return None
        
    df = df.sort_values(by='timestamp')
    df['returns'] = df['price_usd'].pct_change()
    
    volatility = df['returns'].std()
    
    # Scale volatility to a 1-100 score (arbitrary scaling for example purposes)
    # Annualized approx volatility if daily data
    annualized_vol = volatility * np.sqrt(365)
    
    # Cap score at 100
    risk_score = min(100, int(annualized_vol * 100))
    
    return {
        "volatility": volatility,
        "annualized_volatility": annualized_vol,
        "risk_score": risk_score,
        "risk_level": "High" if risk_score > 70 else "Medium" if risk_score > 40 else "Low"
    }
