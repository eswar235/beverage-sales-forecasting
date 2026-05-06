"""
Generate sample beverage sales dataset for demonstration
This creates a realistic dataset with seasonality, trend, and state-level variations
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define states
states = ['California', 'Texas', 'Florida', 'New York', 'Illinois', 
          'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']

# Generate date range from 2019 to 2023
start_date = datetime(2019, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='W-MON')

# Create dataset
data = []

for state in states:
    # Base sales level varies by state
    base_sales = np.random.uniform(5000, 15000)
    
    # Trend component (increasing over time)
    trend = np.linspace(0, base_sales * 0.3, len(date_range))
    
    for idx, date in enumerate(date_range):
        # Seasonal component (higher in summer)
        month = date.month
        seasonal = base_sales * 0.2 * np.sin(2 * np.pi * (month - 1) / 12)
        
        # Weekly pattern (higher on weekends)
        day_of_week = date.dayofweek
        weekly = base_sales * 0.1 * (1 if day_of_week >= 5 else 0)
        
        # Random noise
        noise = np.random.normal(0, base_sales * 0.1)
        
        # Calculate total sales
        total = base_sales + trend[idx] + seasonal + weekly + noise
        total = max(0, total)  # Ensure non-negative
        
        data.append({
            'State': state,
            'Date': date.strftime('%Y-%m-%d'),
            'Total': round(total, 2),
            'Category': 'Beverages'
        })

# Create DataFrame
df = pd.DataFrame(data)

# Randomly remove some dates to simulate missing data (5% missing)
missing_indices = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
df = df.drop(missing_indices)

# Save to CSV
df.to_csv('forecasting_system/data/beverage_sales.csv', index=False)
print(f"Dataset created with {len(df)} records")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"States: {df['State'].nunique()}")
print(f"\nFirst few rows:")
print(df.head(10))
print(f"\nDataset info:")
print(df.info())
