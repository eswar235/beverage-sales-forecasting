"""Data preprocessing module for time series forecasting."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Handles data loading, cleaning, and preprocessing."""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.states = None
        
    def load_data(self):
        """Load data from CSV file."""
        logger.info(f"Loading data from {self.filepath}")
        self.df = pd.read_csv(self.filepath)
        
        # Convert Date column to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%m/%d/%y')
        
        # Sort by State and Date
        self.df = self.df.sort_values(['State', 'Date']).reset_index(drop=True)
        
        self.states = self.df['State'].unique()
        logger.info(f"Loaded {len(self.df)} records for {len(self.states)} states")
        logger.info(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        
        return self.df
    
    def handle_missing_dates(self, state_df):
        """Fill missing dates for a specific state."""
        # If no missing dates, return as is
        if len(state_df) == 0:
            return state_df
        
        # Create complete date range
        min_date = state_df['Date'].min()
        max_date = state_df['Date'].max()
        
        # Determine frequency (weekly or daily)
        date_diff = state_df['Date'].diff().dropna()
        if len(date_diff) > 0:
            median_diff = date_diff.median()
            if median_diff.days >= 6 and median_diff.days <= 8:
                # Weekly data - use the actual dates from the data
                # Don't create a new date range, just check for gaps
                expected_dates = pd.date_range(start=min_date, end=max_date, freq='7D')
                
                # If we have all expected dates, return as is
                if len(state_df) >= len(expected_dates) * 0.95:  # Allow 5% tolerance
                    return state_df[['Date', 'State', 'Category', 'Total']]
            else:
                freq = 'D'
                expected_dates = pd.date_range(start=min_date, end=max_date, freq=freq)
        else:
            # Only one date, return as is
            return state_df[['Date', 'State', 'Category', 'Total']]
        
        # Create complete dataframe with expected dates
        complete_df = pd.DataFrame({'Date': expected_dates})
        complete_df['State'] = state_df['State'].iloc[0]
        complete_df['Category'] = 'Beverages'
        
        # Merge with existing data
        merged_df = complete_df.merge(state_df[['State', 'Date', 'Category', 'Total']], 
                                      on=['State', 'Date', 'Category'], how='left')
        
        return merged_df
    
    def handle_missing_values(self, state_df):
        """Impute missing values using forward fill and interpolation."""
        # Forward fill first
        state_df['Total'] = state_df['Total'].ffill()
        
        # Then interpolate remaining
        state_df['Total'] = state_df['Total'].interpolate(method='linear')
        
        # If still any missing (at the beginning), backfill
        state_df['Total'] = state_df['Total'].bfill()
        
        return state_df
    
    def preprocess_state_data(self, state):
        """Complete preprocessing pipeline for a single state."""
        logger.info(f"Preprocessing data for {state}")
        
        # Filter data for specific state
        state_df = self.df[self.df['State'] == state].copy()
        
        # Handle missing dates
        state_df = self.handle_missing_dates(state_df)
        
        # Handle missing values
        state_df = self.handle_missing_values(state_df)
        
        # Ensure sorted by date
        state_df = state_df.sort_values('Date').reset_index(drop=True)
        
        logger.info(f"Preprocessed {len(state_df)} records for {state}")
        
        return state_df
    
    def preprocess_all_states(self):
        """Preprocess data for all states."""
        if self.df is None:
            self.load_data()
        
        preprocessed_data = {}
        
        for state in self.states:
            preprocessed_data[state] = self.preprocess_state_data(state)
        
        return preprocessed_data
    
    def get_train_test_split(self, state_df, test_weeks=8):
        """Split data into train and test sets (time-based split)."""
        # Calculate split point
        split_idx = len(state_df) - test_weeks
        
        train_df = state_df.iloc[:split_idx].copy()
        test_df = state_df.iloc[split_idx:].copy()
        
        logger.info(f"Train set: {len(train_df)} records, Test set: {len(test_df)} records")
        
        return train_df, test_df


if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = DataPreprocessor('../data/beverage_sales.csv')
    preprocessor.load_data()
    
    # Test preprocessing for California
    ca_data = preprocessor.preprocess_state_data('California')
    print("\nCalifornia data:")
    print(ca_data.head())
    print(f"\nShape: {ca_data.shape}")
    print(f"Missing values: {ca_data['Total'].isna().sum()}")
