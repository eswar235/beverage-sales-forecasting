"""LSTM model implementation for time series forecasting."""
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LSTMForecaster:
    """LSTM forecasting model."""
    
    def __init__(self, lookback=8, units=50, dropout=0.2):
        self.lookback = lookback
        self.units = units
        self.dropout = dropout
        self.model = None
        self.scaler = MinMaxScaler()
        self.history = None
    
    def create_sequences(self, data):
        """Create sequences for LSTM training."""
        X, y = [], []
        
        for i in range(len(data) - self.lookback):
            X.append(data[i:i + self.lookback])
            y.append(data[i + self.lookback])
        
        return np.array(X), np.array(y)
    
    def train(self, train_data, epochs=50, batch_size=32, validation_split=0.1):
        """Train LSTM model."""
        logger.info("Training LSTM model...")
        
        # Extract series
        if isinstance(train_data, pd.DataFrame):
            series = train_data['Total'].values
        else:
            series = train_data.values
        
        # Reshape for scaling
        series = series.reshape(-1, 1)
        
        # Scale data
        scaled_data = self.scaler.fit_transform(series)
        
        # Create sequences
        X, y = self.create_sequences(scaled_data)
        
        # Reshape for LSTM [samples, timesteps, features]
        X = X.reshape(X.shape[0], X.shape[1], 1)
        
        logger.info(f"Training data shape: X={X.shape}, y={y.shape}")
        
        # Build model
        self.model = Sequential([
            LSTM(self.units, return_sequences=True, input_shape=(self.lookback, 1)),
            Dropout(self.dropout),
            LSTM(self.units, return_sequences=False),
            Dropout(self.dropout),
            Dense(25),
            Dense(1)
        ])
        
        # Compile model
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        
        # Train model
        self.history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=0
        )
        
        logger.info("LSTM model trained successfully")
        
        return self
    
    def predict(self, last_sequence, steps=8):
        """Make predictions."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare last sequence
        if isinstance(last_sequence, pd.DataFrame):
            last_data = last_sequence['Total'].values[-self.lookback:]
        else:
            last_data = last_sequence[-self.lookback:]
        
        # Scale
        last_data = last_data.reshape(-1, 1)
        last_scaled = self.scaler.transform(last_data)
        
        # Make predictions
        predictions = []
        current_sequence = last_scaled.copy()
        
        for _ in range(steps):
            # Reshape for prediction
            X_pred = current_sequence.reshape(1, self.lookback, 1)
            
            # Predict
            pred_scaled = self.model.predict(X_pred, verbose=0)
            
            # Inverse transform
            pred = self.scaler.inverse_transform(pred_scaled)[0, 0]
            predictions.append(pred)
            
            # Update sequence
            current_sequence = np.append(current_sequence[1:], pred_scaled).reshape(-1, 1)
        
        return np.array(predictions)
    
    def get_training_history(self):
        """Get training history."""
        if self.history is None:
            return None
        
        return pd.DataFrame(self.history.history)
