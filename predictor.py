import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

class PricePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, df: pd.DataFrame):
        """
        Trains a simple linear regression model on historical price data.
        Assumes df has columns: 'timestamp', 'price_usd', 'total_volume'.
        """
        if df.empty or len(df) < 10:
            return False, "Not enough data"

        # Prepare features (e.g., predicting price based on timestamp and volume)
        df = df.sort_values(by='timestamp')
        df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days
        
        X = df[['days_since_start', 'total_volume']]
        y = df['price_usd']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        
        return True, f"Model trained. MSE: {mse:.4f}"

    def predict(self, future_days: int, current_volume: float, days_since_start: int):
        """
        Predicts future price.
        """
        target_day = days_since_start + future_days
        X_future = pd.DataFrame({'days_since_start': [target_day], 'total_volume': [current_volume]})
        predicted_price = self.model.predict(X_future)[0]
        return max(0, predicted_price) # Prevent negative prices
