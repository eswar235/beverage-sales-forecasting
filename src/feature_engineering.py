"""Feature engineering module for time series forecasting."""
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Creates features for time series forecasting."""
    
    def __init__(self):
        pass
    
    def create_lag_features(self, df, lags=[1, 2, 4]):
        """Create lag features."""
        df = df.copy()
        
        for lag in lags:
            df[f'lag_{lag}'] = df['Total'].shift(lag)
        
        return df
    
    def create_rolling_features(self, df, windows=[4, 8]):
        """Create rolling mean and std features."""
        df = df.copy()
        
        for window in windows:
            df[f'rolling_mean_{window}'] = df['Total'].rolling(window=window, min_periods=1).mean()
            df[f'rolling_std_{window}'] = df['Total'].rolling(window=window, min_periods=1).std()
        
        return df
    
    def create_temporal_features(self, df):
        """Create temporal features from date."""
        df = df.copy()
        
        df['day_of_week'] = df['Date'].dt.dayofweek
        df['day_of_month'] = df['Date'].dt.day
        df['week_of_year'] = df['Date'].dt.isocalendar().week
        df['month'] = df['Date'].dt.month
        df['quarter'] = df['Date'].dt.quarter
        df['year'] = df['Date'].dt.year
        
        # Cyclical encoding for month and day_of_week
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        return df
    
    def create_trend_features(self, df):
        """Create trend features."""
        df = df.copy()
        
        # Linear trend
        df['trend'] = np.arange(len(df))
        
        # Polynomial trend
        df['trend_squared'] = df['trend'] ** 2
        
        return df
    
    def create_all_features(self, df):
        """Create all features."""
        logger.info("Creating all features...")
        
        df = df.copy()
        
        # Create features
        df = self.create_lag_features(df)
        df = self.create_rolling_features(df)
        df = self.create_temporal_features(df)
        df = self.create_trend_features(df)
        
        logger.info(f"Created {len(df.columns) - 4} features")
        
        return df
    
    def get_feature_columns(self, df):
        """Get list of feature columns (excluding target and metadata)."""
        exclude_cols = ['Date', 'State', 'Category', 'Total']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        return feature_cols
    
    def prepare_ml_data(self, df, target_col='Total'):
        """Prepare data for ML models (remove NaN rows from lag features)."""
        df = df.copy()
        
        # Get feature columns
        feature_cols = self.get_feature_columns(df)
        
        # Remove rows with NaN in features (from lag features)
        df_clean = df.dropna(subset=feature_cols)
        
        X = df_clean[feature_cols]
        y = df_clean[target_col]
        dates = df_clean['Date']
        
        logger.info(f"Prepared ML data: {len(X)} samples, {len(feature_cols)} features")
        
        return X, y, dates, df_clean


if __name__ == "__main__":
    # Test feature engineering
    from data_preprocessing import DataPreprocessor
    
    preprocessor = DataPreprocessor('../data/beverage_sales.csv')
    preprocessor.load_data()
    ca_data = preprocessor.preprocess_state_data('California')
    
    engineer = FeatureEngineer()
    ca_features = engineer.create_all_features(ca_data)
    
    print("\nFeatures created:")
    print(ca_features.columns.tolist())
    print(f"\nShape: {ca_features.shape}")
    print("\nFirst few rows:")
    print(ca_features.head())
