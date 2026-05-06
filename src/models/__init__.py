"""Forecasting models package"""
from .arima_model import ARIMAForecaster
from .prophet_model import ProphetForecaster
from .xgboost_model import XGBoostForecaster

# Try to import LSTM, but don't fail if TensorFlow is not available
try:
    from .lstm_model import LSTMForecaster
    LSTM_AVAILABLE = True
except ImportError as e:
    LSTMForecaster = None
    LSTM_AVAILABLE = False
    print(f"Warning: LSTM model not available. TensorFlow import failed: {e}")

__all__ = ['ARIMAForecaster', 'ProphetForecaster', 'XGBoostForecaster', 'LSTM_AVAILABLE']
if LSTM_AVAILABLE:
    __all__.append('LSTMForecaster')
