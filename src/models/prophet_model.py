"""Facebook Prophet model implementation."""
import pandas as pd
import numpy as np
from prophet import Prophet
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProphetForecaster:
    """Facebook Prophet forecasting model."""
    
    def __init__(self, yearly_seasonality=True, weekly_seasonality=True, 
                 daily_seasonality=False):
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality
        self.model = None
    
    def prepare_data(self, train_data):
        """Prepare data in Prophet format (ds, y columns)."""
        if isinstance(train_data, pd.DataFrame):
            df = train_data[['Date', 'Total']].copy()
        else:
            df = pd.DataFrame({'Date': train_data.index, 'Total': train_data.values})
        
        df.columns = ['ds', 'y']
        return df
    
    def train(self, train_data):
        """Train Prophet model."""
        logger.info("Training Prophet model...")
        
        # Prepare data
        df = self.prepare_data(train_data)
        
        # Initialize model
        self.model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05
        )
        
        # Add custom seasonalities
        self.model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        
        # Fit model
        self.model.fit(df)
        
        logger.info("Prophet model trained successfully")
        
        return self
    
    def predict(self, steps=8, freq='W'):
        """Make predictions."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=steps, freq=freq)
        
        # Make predictions
        forecast = self.model.predict(future)
        
        # Return only future predictions
        predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(steps)
        
        return predictions['yhat'].values
    
    def get_forecast_dataframe(self, steps=8, freq='W'):
        """Get full forecast dataframe with confidence intervals."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        future = self.model.make_future_dataframe(periods=steps, freq=freq)
        forecast = self.model.predict(future)
        
        return forecast.tail(steps)
