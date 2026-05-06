"""Generate realistic time series data from the single snapshot."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_time_series():
    """Generate weekly time series data from 2019-01-12 to 2022-12-31."""
    
    # Load the base data
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'beverage_sales_original.csv')
    
    # First, backup the original file
    original_file = os.path.join(script_dir, 'beverage_sales.csv')
    if os.path.exists(original_file) and not os.path.exists(input_file):
        import shutil
        shutil.copy(original_file, input_file)
        print(f"Backed up original file to beverage_sales_original.csv")
    
    df = pd.read_csv(input_file if os.path.exists(input_file) else original_file)
    print(f"Loaded {len(df)} states")
    
    # Generate weekly dates from 2019-01-12 to 2022-12-31
    start_date = datetime(2019, 1, 12)
    end_date = datetime(2022, 12, 31)
    
    # Create weekly date range
    dates = pd.date_range(start=start_date, end=end_date, freq='W-SAT')
    print(f"Generated {len(dates)} weekly dates")
    
    # Create time series for each state
    all_data = []
    
    for _, row in df.iterrows():
        state = row['State']
        base_sales = row['Total']
        
        print(f"Generating data for {state}...")
        
        # Generate realistic time series with:
        # 1. Overall trend (slight growth)
        # 2. Yearly seasonality (peaks in summer)
        # 3. Random noise
        
        for i, date in enumerate(dates):
            # Trend component (1-2% annual growth)
            years_elapsed = i / 52.0
            trend = 1 + (0.015 * years_elapsed)
            
            # Seasonal component (higher in summer, lower in winter)
            month = date.month
            if month in [6, 7, 8]:  # Summer peak
                seasonal = 1.15
            elif month in [12, 1, 2]:  # Winter low
                seasonal = 0.90
            elif month in [3, 4, 5]:  # Spring
                seasonal = 1.05
            else:  # Fall
                seasonal = 1.00
            
            # Weekly pattern (slightly higher on weekends)
            week_of_year = date.isocalendar()[1]
            weekly_pattern = 1 + 0.05 * np.sin(2 * np.pi * week_of_year / 52)
            
            # Random noise (-5% to +5%)
            noise = np.random.uniform(0.95, 1.05)
            
            # Calculate sales
            sales = base_sales * trend * seasonal * weekly_pattern * noise
            
            # Add some random events (spikes or drops)
            if np.random.random() < 0.05:  # 5% chance of event
                event_multiplier = np.random.choice([0.85, 1.20])  # Drop or spike
                sales *= event_multiplier
            
            all_data.append({
                'State': state,
                'Date': date.strftime('%m/%d/%y'),
                'Total': int(sales),
                'Category': 'Beverages'
            })
    
    # Create dataframe
    ts_df = pd.DataFrame(all_data)
    
    # Save to CSV
    output_file = os.path.join(script_dir, 'beverage_sales.csv')
    ts_df.to_csv(output_file, index=False)
    
    print(f"\nGenerated {len(ts_df)} records")
    print(f"Saved to {output_file}")
    
    # Print summary
    print("\nSummary:")
    print(f"States: {ts_df['State'].nunique()}")
    print(f"Date range: {ts_df['Date'].min()} to {ts_df['Date'].max()}")
    print(f"Records per state: {len(ts_df) // ts_df['State'].nunique()}")
    print(f"Total sales: ${ts_df['Total'].sum():,.0f}")

if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility
    generate_time_series()
