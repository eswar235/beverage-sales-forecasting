"""Complete training pipeline for all forecasting models."""
import pandas as pd
import numpy as np
import logging
import pickle
import json
from pathlib import Path

from data_preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from model_comparison import ModelComparator
from models.arima_model import ARIMAForecaster
from models.prophet_model import ProphetForecaster
from models.xgboost_model import XGBoostForecaster
from models.lstm_model import LSTMForecaster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ForecastingPipeline:
    """Complete forecasting pipeline."""
    
    def __init__(self, data_path, state='California', test_weeks=8):
        self.data_path = data_path
        self.state = state
        self.test_weeks = test_weeks
        
        # Initialize components
        self.preprocessor = DataPreprocessor(data_path)
        self.engineer = FeatureEngineer()
        self.comparator = ModelComparator()
        
        # Models
        self.models = {}
        self.predictions = {}
        self.best_model_name = None
        
    def load_and_preprocess(self):
        """Load and preprocess data."""
        logger.info(f"Loading and preprocessing data for {self.state}...")
        
        # Load data
        self.preprocessor.load_data()
        
        # Preprocess state data
        self.state_data = self.preprocessor.preprocess_state_data(self.state)
        
        # Split into train and test
        self.train_data, self.test_data = self.preprocessor.get_train_test_split(
            self.state_data, test_weeks=self.test_weeks
        )
        
        logger.info(f"Train size: {len(self.train_data)}, Test size: {len(self.test_data)}")
        
        return self
    
    def create_features(self):
        """Create features for ML models."""
        logger.info("Creating features...")
        
        # Create features for full dataset
        self.state_features = self.engineer.create_all_features(self.state_data)
        
        # Prepare ML data
        X, y, dates, df_clean = self.engineer.prepare_ml_data(self.state_features)
        
        # Split into train and test based on dates
        train_mask = dates.isin(self.train_data['Date'])
        
        self.X_train = X[train_mask]
        self.y_train = y[train_mask]
        self.X_test = X[~train_mask]
        self.y_test = y[~train_mask]
        
        logger.info(f"Feature matrix: {self.X_train.shape}")
        
        return self
    
    def train_arima(self):
        """Train ARIMA model."""
        logger.info("\n" + "="*50)
        logger.info("Training ARIMA Model")
        logger.info("="*50)
        
        try:
            arima = ARIMAForecaster(seasonal=True, seasonal_period=52)
            arima.train(self.train_data, auto_order=False)
            
            # Predict
            predictions = arima.predict(steps=self.test_weeks)
            
            # Store
            self.models['ARIMA'] = arima
            self.predictions['ARIMA'] = predictions
            
            # Evaluate
            self.comparator.calculate_metrics(
                self.test_data['Total'].values,
                predictions,
                'ARIMA'
            )
            
        except Exception as e:
            logger.error(f"ARIMA training failed: {e}")
        
        return self
    
    def train_prophet(self):
        """Train Prophet model."""
        logger.info("\n" + "="*50)
        logger.info("Training Prophet Model")
        logger.info("="*50)
        
        try:
            prophet = ProphetForecaster()
            prophet.train(self.train_data)
            
            # Predict
            predictions = prophet.predict(steps=self.test_weeks, freq='W')
            
            # Store
            self.models['Prophet'] = prophet
            self.predictions['Prophet'] = predictions
            
            # Evaluate
            self.comparator.calculate_metrics(
                self.test_data['Total'].values,
                predictions,
                'Prophet'
            )
            
        except Exception as e:
            logger.error(f"Prophet training failed: {e}")
        
        return self
    
    def train_xgboost(self):
        """Train XGBoost model."""
        logger.info("\n" + "="*50)
        logger.info("Training XGBoost Model")
        logger.info("="*50)
        
        try:
            xgb_model = XGBoostForecaster(n_estimators=100, learning_rate=0.1, max_depth=5)
            xgb_model.train(self.X_train, self.y_train)
            
            # Predict
            predictions = xgb_model.predict(self.X_test)
            
            # Store
            self.models['XGBoost'] = xgb_model
            self.predictions['XGBoost'] = predictions
            
            # Evaluate
            self.comparator.calculate_metrics(
                self.y_test.values,
                predictions,
                'XGBoost'
            )
            
            # Show feature importance
            importance = xgb_model.get_feature_importance()
            logger.info("\nTop 10 Important Features:")
            logger.info(importance.head(10).to_string())
            
        except Exception as e:
            logger.error(f"XGBoost training failed: {e}")
        
        return self
    
    def train_lstm(self):
        """Train LSTM model."""
        logger.info("\n" + "="*50)
        logger.info("Training LSTM Model")
        logger.info("="*50)
        
        try:
            lstm = LSTMForecaster(lookback=8, units=50, dropout=0.2)
            lstm.train(self.train_data, epochs=50, batch_size=16)
            
            # Predict
            predictions = lstm.predict(self.train_data, steps=self.test_weeks)
            
            # Store
            self.models['LSTM'] = lstm
            self.predictions['LSTM'] = predictions
            
            # Evaluate
            self.comparator.calculate_metrics(
                self.test_data['Total'].values,
                predictions,
                'LSTM'
            )
            
        except Exception as e:
            logger.error(f"LSTM training failed: {e}")
        
        return self
    
    def train_all_models(self):
        """Train all models."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Training All Models for {self.state}")
        logger.info(f"{'='*60}\n")
        
        # Train each model
        self.train_arima()
        self.train_prophet()
        self.train_xgboost()
        self.train_lstm()
        
        return self
    
    def compare_models(self):
        """Compare all models and select best."""
        logger.info("\n" + "="*60)
        logger.info("Model Comparison")
        logger.info("="*60)
        
        # Get comparison table
        comparison_df = self.comparator.get_comparison_table()
        logger.info("\n" + comparison_df.to_string())
        
        # Get best model
        self.best_model_name = self.comparator.get_best_model(metric='RMSE')
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Best Model: {self.best_model_name}")
        logger.info(f"{'='*60}")
        
        return self
    
    def save_models(self, output_dir='../models'):
        """Save trained models."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\nSaving models to {output_dir}...")
        
        for model_name, model in self.models.items():
            model_file = output_path / f"{self.state}_{model_name}.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"Saved {model_name} to {model_file}")
        
        # Save comparison results
        comparison_df = self.comparator.get_comparison_table()
        comparison_file = output_path / f"{self.state}_comparison.csv"
        comparison_df.to_csv(comparison_file)
        logger.info(f"Saved comparison results to {comparison_file}")
        
        # Save metadata
        metadata = {
            'state': self.state,
            'test_weeks': self.test_weeks,
            'best_model': self.best_model_name,
            'train_size': len(self.train_data),
            'test_size': len(self.test_data)
        }
        
        metadata_file = output_path / f"{self.state}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved metadata to {metadata_file}")
        
        return self
    
    def run(self):
        """Run complete pipeline."""
        self.load_and_preprocess()
        self.create_features()
        self.train_all_models()
        self.compare_models()
        self.save_models()
        
        logger.info("\n" + "="*60)
        logger.info("Pipeline Complete!")
        logger.info("="*60)
        
        return self


if __name__ == "__main__":
    # Run pipeline for California
    pipeline = ForecastingPipeline(
        data_path='../data/beverage_sales.csv',
        state='California',
        test_weeks=8
    )
    
    pipeline.run()
