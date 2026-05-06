"""XGBoost model implementation with lag features."""
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XGBoostForecaster:
    """XGBoost forecasting model with lag features."""
    
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=5):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.model = None
        self.feature_names = None
    
    def train(self, X_train, y_train):
        """Train XGBoost model."""
        logger.info("Training XGBoost model...")
        
        # Store feature names
        self.feature_names = X_train.columns.tolist()
        
        # Initialize model
        self.model = xgb.XGBRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=42,
            objective='reg:squarederror'
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        logger.info(f"XGBoost model trained with {len(self.feature_names)} features")
        
        return self
    
    def predict(self, X_test):
        """Make predictions."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        predictions = self.model.predict(X_test)
        
        return predictions
    
    def get_feature_importance(self):
        """Get feature importance."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance
