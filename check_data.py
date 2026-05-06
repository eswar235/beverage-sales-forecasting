"""Script to check and analyze the beverage sales dataset."""
import pandas as pd
import numpy as np
from pathlib import Path

def check_dataset():
    """Analyze the dataset and print summary statistics."""
    
    # Load data
    data_path = Path(__file__).parent / 'data' / 'beverage_sales.csv'
    print(f"Loading data from: {data_path}")
    print("=" * 70)
    
    df = pd.read_csv(data_path)
    
    # Basic info
    print("\n1. BASIC INFORMATION")
    print("-" * 70)
    print(f"Total records: {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes}")
    
    # Date range
    print("\n2. DATE RANGE")
    print("-" * 70)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    print(f"Start date: {df['Date'].min()}")
    print(f"End date: {df['Date'].max()}")
    print(f"Date range: {(df['Date'].max() - df['Date'].min()).days} days")
    
    # States
    print("\n3. STATES")
    print("-" * 70)
    states = df['State'].unique()
    print(f"Number of states: {len(states)}")
    print(f"States: {', '.join(sorted(states))}")
    
    # Records per state
    print("\n4. RECORDS PER STATE")
    print("-" * 70)
    records_per_state = df.groupby('State').size()
    print(f"Min records: {records_per_state.min()}")
    print(f"Max records: {records_per_state.max()}")
    print(f"Average records: {records_per_state.mean():.1f}")
    
    # Sales statistics
    print("\n5. SALES STATISTICS")
    print("-" * 70)
    print(f"Total sales (all states, all time): ${df['Total'].sum():,.0f}")
    print(f"Average weekly sales: ${df['Total'].mean():,.0f}")
    print(f"Median weekly sales: ${df['Total'].median():,.0f}")
    print(f"Min weekly sales: ${df['Total'].min():,.0f}")
    print(f"Max weekly sales: ${df['Total'].max():,.0f}")
    print(f"Std deviation: ${df['Total'].std():,.0f}")
    
    # Top states by average sales
    print("\n6. TOP 10 STATES BY AVERAGE SALES")
    print("-" * 70)
    top_states = df.groupby('State')['Total'].mean().sort_values(ascending=False).head(10)
    for i, (state, avg_sales) in enumerate(top_states.items(), 1):
        print(f"{i:2d}. {state:20s} ${avg_sales:,.0f}")
    
    # Missing values
    print("\n7. DATA QUALITY")
    print("-" * 70)
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    
    # Sample data
    print("\n8. SAMPLE DATA (First 5 rows)")
    print("-" * 70)
    print(df.head().to_string())
    
    # Check for date gaps (using California as example)
    print("\n9. DATE CONTINUITY CHECK (California)")
    print("-" * 70)
    ca_data = df[df['State'] == 'California'].sort_values('Date')
    date_diffs = ca_data['Date'].diff().dt.days
    print(f"Most common gap between dates: {date_diffs.mode().values[0]} days")
    print(f"Min gap: {date_diffs.min()} days")
    print(f"Max gap: {date_diffs.max()} days")
    
    # Frequency detection
    if date_diffs.mode().values[0] == 7:
        print("Data frequency: WEEKLY")
    elif date_diffs.mode().values[0] == 1:
        print("Data frequency: DAILY")
    else:
        print(f"Data frequency: IRREGULAR ({date_diffs.mode().values[0]} days)")
    
    print("\n" + "=" * 70)
    print("Dataset check complete!")
    print("=" * 70)

if __name__ == "__main__":
    check_dataset()
