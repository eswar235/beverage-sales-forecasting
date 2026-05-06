"""ARIMA/SARIMA model implementation."""
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ARIMAForecaster:
    """ARIMA/SARIMA forecasting model."""
    
    def __init__(self, seasonal=True, seasonal_period=52):
        self.seasonal = seasonal
        self.seasonal_period = seasonal_period
        self.model = None
        self.model_fit = None
        self.best_order = None
        self.best_seasonal_order = None
    
    def check_stationarity(self, series):
        """Check if series is stationary using ADF test."""
        result = adfuller(series.dropna())
        logger.info(f"ADF Statistic: {result[0]:.4f}")
        logger.info(f"p-value: {result[1]:.4f}")
        
        return result[1] < 0.05
    
    def find_best_order(self, series, max_p=3, max_d=2, max_q=3):
        """Find best ARIMA order using AIC."""
        logger.info("Finding best ARIMA order...")
        
        best_aic = np.inf
        best_order = None
        
        for p in range(max_p + 1):
            for d in range(max_d + 1):
                for q in range(max_q + 1):
                    try:
                        if self.seasonal:
                            model = SARIMAX(series, 
                                          order=(p, d, q),
                                          seasonal_order=(1, 1, 1, self.seasonal_period),
                                          enforce_stationarity=False,
                                          enforce_invertibility=False)
                        else:
                            model = SARIMAX(series, 
                                          order=(p, d, q),
                                          enforce_stationarity=False,
                                          enforce_invertibility=False)
                        
                        results = model.fit(disp=False)
                        
                        if results.aic < best_aic:
                            best_aic = results.aic
                            best_order = (p, d, q)
                    
                    except:
                        continue
        
        logger.info(f"Best order: {best_order} with AIC: {best_aic:.2f}")
        return best_order
    
    def train(self, train_data, auto_order=False):
        """Train ARIMA/SARIMA model."""
        logger.info("Training ARIMA/SARIMA model...")
        
        # Extract series
        if isinstance(train_data, pd.DataFrame):
            series = train_data['Total']
        else:
            series = train_data
        
        # Check stationarity
        is_stationary = self.check_stationarity(series)
        logger.info(f"Series is {'stationary' if is_stationary else 'non-stationary'}")
        
        # Find best order if auto_order is True
        if auto_order:
            self.best_order = self.find_best_order(series)
        else:
            self.best_order = (1, 1, 1)  # Default order
        
        # Set seasonal order
        if self.seasonal:
            self.best_seasonal_order = (1, 1, 1, self.seasonal_period)
        else:
            self.best_seasonal_order = (0, 0, 0, 0)
        
        # Train model
        self.model = SARIMAX(series,
                            order=self.best_order,
                            seasonal_order=self.best_seasonal_order,
                            enforce_stationarity=False,
                            enforce_invertibility=False)
        
        self.model_fit = self.model.fit(disp=False)
        
        logger.info(f"Model trained with order {self.best_order}")
        logger.info(f"AIC: {self.model_fit.aic:.2f}")
        
        return self
    
    def predict(self, steps=8):
        """Make predictions."""
        if self.model_fit is None:
            raise ValueError("Model not trained. Call train() first.")
        
        forecast = self.model_fit.forecast(steps=steps)
        
        return forecast.values
    
    def get_model_summary(self):
        """Get model summary."""
        if self.model_fit is None:
            return None
        
        return self.model_fit.summary()
