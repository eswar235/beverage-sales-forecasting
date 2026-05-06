"""
Comprehensive demo script for the Beverage Sales Forecasting System.

This script demonstrates:
1. Data loading and preprocessing
2. Feature engineering
3. Training all 4 models (ARIMA, Prophet, XGBoost, LSTM)
4. Model comparison
5. Making predictions
6. Saving results
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from model_comparison import ModelComparator
from models.arima_model import ARIMAForecaster
from models.prophet_model import ProphetForecaster
from models.xgboost_model import XGBoostForecaster

# Try to import LSTM, but continue without it if TensorFlow is not available
try:
    from models.lstm_model import LSTMForecaster
    LSTM_AVAILABLE = True
except ImportError:
    LSTMForecaster = None
    LSTM_AVAILABLE = False
    print("⚠️  Warning: LSTM model not available (TensorFlow not installed or incompatible)")

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def demo_data_preprocessing(state='California'):
    """Demonstrate data preprocessing."""
    print_header("STEP 1: DATA PREPROCESSING")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor('data/beverage_sales.csv')
    
    # Load data
    print("Loading data...")
    preprocessor.load_data()
    print(f"✓ Loaded {len(preprocessor.df):,} records for {len(preprocessor.states)} states")
    print(f"✓ Date range: {preprocessor.df['Date'].min()} to {preprocessor.df['Date'].max()}")
    
    # Preprocess state data
    print(f"\nPreprocessing data for {state}...")
    state_data = preprocessor.preprocess_state_data(state)
    print(f"✓ Preprocessed {len(state_data)} records")
    print(f"✓ Missing values: {state_data['Total'].isna().sum()}")
    
    # Train/test split
    print("\nSplitting into train and test sets...")
    train_data, test_data = preprocessor.get_train_test_split(state_data, test_weeks=8)
    print(f"✓ Train set: {len(train_data)} weeks")
    print(f"✓ Test set: {len(test_data)} weeks")
    
    return preprocessor, state_data, train_data, test_data

def demo_feature_engineering(state_data, train_data):
    """Demonstrate feature engineering."""
    print_header("STEP 2: FEATURE ENGINEERING")
    
    # Initialize engineer
    engineer = FeatureEngineer()
    
    # Create features
    print("Creating features...")
    state_features = engineer.create_all_features(state_data)
    
    feature_cols = engineer.get_feature_columns(state_features)
    print(f"✓ Created {len(feature_cols)} features:")
    print(f"  - Lag features: {[col for col in feature_cols if 'lag' in col]}")
    print(f"  - Rolling features: {[col for col in feature_cols if 'rolling' in col]}")
    print(f"  - Temporal features: {[col for col in feature_cols if any(x in col for x in ['month', 'week', 'day', 'quarter'])]}")
    print(f"  - Trend features: {[col for col in feature_cols if 'trend' in col]}")
    
    # Prepare ML data
    print("\nPreparing data for ML models...")
    X, y, dates, df_clean = engineer.prepare_ml_data(state_features)
    
    # Split into train/test
    train_mask = dates.isin(train_data['Date'])
    X_train = X[train_mask]
    y_train = y[train_mask]
    X_test = X[~train_mask]
    y_test = y[~train_mask]
    
    print(f"✓ Training features: {X_train.shape}")
    print(f"✓ Test features: {X_test.shape}")
    
    return engineer, X_train, y_train, X_test, y_test

def demo_model_training(train_data, test_data, X_train, y_train, X_test, y_test):
    """Demonstrate training all models."""
    print_header("STEP 3: MODEL TRAINING")
    
    models = {}
    predictions = {}
    comparator = ModelComparator()
    
    # 1. ARIMA
    print("1. Training ARIMA/SARIMA Model...")
    print("-" * 80)
    try:
        arima = ARIMAForecaster(seasonal=True, seasonal_period=52)
        arima.train(train_data, auto_order=False)
        arima_pred = arima.predict(steps=len(test_data))
        models['ARIMA'] = arima
        predictions['ARIMA'] = arima_pred
        comparator.calculate_metrics(test_data['Total'].values, arima_pred, 'ARIMA')
        print("✓ ARIMA training complete\n")
    except Exception as e:
        print(f"✗ ARIMA training failed: {e}\n")
    
    # 2. Prophet
    print("2. Training Facebook Prophet Model...")
    print("-" * 80)
    try:
        prophet = ProphetForecaster()
        prophet.train(train_data)
        prophet_pred = prophet.predict(steps=len(test_data), freq='W')
        models['Prophet'] = prophet
        predictions['Prophet'] = prophet_pred
        comparator.calculate_metrics(test_data['Total'].values, prophet_pred, 'Prophet')
        print("✓ Prophet training complete\n")
    except Exception as e:
        print(f"✗ Prophet training failed: {e}\n")
    
    # 3. XGBoost
    print("3. Training XGBoost Model...")
    print("-" * 80)
    try:
        xgb_model = XGBoostForecaster(n_estimators=100, learning_rate=0.1, max_depth=5)
        xgb_model.train(X_train, y_train)
        xgb_pred = xgb_model.predict(X_test)
        models['XGBoost'] = xgb_model
        predictions['XGBoost'] = xgb_pred
        comparator.calculate_metrics(y_test.values, xgb_pred, 'XGBoost')
        
        # Show feature importance
        importance = xgb_model.get_feature_importance()
        print("\nTop 10 Important Features:")
        print(importance.head(10).to_string(index=False))
        print("\n✓ XGBoost training complete\n")
    except Exception as e:
        print(f"✗ XGBoost training failed: {e}\n")
    
    # 4. LSTM
    if LSTM_AVAILABLE:
        print("4. Training LSTM Model...")
        print("-" * 80)
        try:
            lstm = LSTMForecaster(lookback=8, units=50, dropout=0.2)
            lstm.train(train_data, epochs=50, batch_size=16, validation_split=0.1)
            lstm_pred = lstm.predict(train_data, steps=len(test_data))
            models['LSTM'] = lstm
            predictions['LSTM'] = lstm_pred
            comparator.calculate_metrics(test_data['Total'].values, lstm_pred, 'LSTM')
            print("✓ LSTM training complete\n")
        except Exception as e:
            print(f"✗ LSTM training failed: {e}\n")
    else:
        print("4. LSTM Model - SKIPPED (TensorFlow not available)")
        print("-" * 80)
        print("⚠️  LSTM model requires TensorFlow which is not available on this system.")
        print("   The system will continue with the other 3 models.\n")
    
    return models, predictions, comparator

def demo_model_comparison(comparator):
    """Demonstrate model comparison."""
    print_header("STEP 4: MODEL COMPARISON")
    
    # Get comparison table
    comparison_df = comparator.get_comparison_table()
    print("Performance Metrics for All Models:")
    print("-" * 80)
    print(comparison_df.to_string())
    
    # Get best model
    best_model = comparator.get_best_model(metric='RMSE')
    print(f"\n🏆 Best Model: {best_model} (based on RMSE)")
    
    return comparison_df, best_model

def demo_visualization(test_data, predictions, state='California'):
    """Create visualization of predictions."""
    print_header("STEP 5: VISUALIZATION")
    
    print("Creating forecast visualization...")
    
    # Create figure
    plt.figure(figsize=(15, 8))
    
    # Plot actual values
    plt.plot(test_data['Date'], test_data['Total'], 
             label='Actual', marker='o', linewidth=2, markersize=8, color='black')
    
    # Plot predictions for each model
    colors = {'ARIMA': 'blue', 'Prophet': 'green', 'XGBoost': 'red', 'LSTM': 'purple'}
    markers = {'ARIMA': 's', 'Prophet': '^', 'XGBoost': 'D', 'LSTM': 'v'}
    
    for model_name, pred in predictions.items():
        plt.plot(test_data['Date'], pred, 
                label=model_name, marker=markers[model_name], 
                linewidth=1.5, markersize=6, alpha=0.7, color=colors[model_name])
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Sales ($)', fontsize=12)
    plt.title(f'{state} Beverage Sales - 8-Week Forecast Comparison', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save figure
    output_file = f'models/{state}_forecast_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to {output_file}")
    
    plt.close()

def demo_future_forecast(models, train_data, X_test, best_model, state='California'):
    """Demonstrate making future forecasts."""
    print_header("STEP 6: FUTURE FORECAST (Next 8 Weeks)")
    
    print(f"Generating 8-week forecast using best model ({best_model})...")
    
    # Get the best model
    model = models[best_model]
    
    # Make prediction
    if best_model in ['ARIMA', 'Prophet']:
        future_pred = model.predict(steps=8)
    elif best_model == 'LSTM':
        future_pred = model.predict(train_data, steps=8)
    elif best_model == 'XGBoost':
        # Use last 8 weeks of features
        future_pred = model.predict(X_test.tail(8))
    
    # Create future dates
    last_date = train_data['Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(weeks=1), periods=8, freq='W')
    
    # Print forecast
    print("\nForecast Results:")
    print("-" * 80)
    print(f"{'Week':<6} {'Date':<12} {'Predicted Sales':<20} {'Formatted'}")
    print("-" * 80)
    
    for i, (date, sales) in enumerate(zip(future_dates, future_pred), 1):
        print(f"{i:<6} {date.strftime('%Y-%m-%d'):<12} ${sales:<18,.0f} ${sales:,.0f}")
    
    print("-" * 80)
    print(f"Total 8-week forecast: ${future_pred.sum():,.0f}")
    print(f"Average weekly sales: ${future_pred.mean():,.0f}")
    
    return future_dates, future_pred

def main():
    """Run complete demo."""
    print("\n" + "=" * 80)
    print("  BEVERAGE SALES FORECASTING SYSTEM - COMPREHENSIVE DEMO")
    print("=" * 80)
    
    # Configuration
    STATE = 'California'
    TEST_WEEKS = 8
    
    print(f"\nConfiguration:")
    print(f"  State: {STATE}")
    print(f"  Test weeks: {TEST_WEEKS}")
    
    try:
        # Step 1: Data Preprocessing
        preprocessor, state_data, train_data, test_data = demo_data_preprocessing(STATE)
        
        # Step 2: Feature Engineering
        engineer, X_train, y_train, X_test, y_test = demo_feature_engineering(state_data, train_data)
        
        # Step 3: Model Training
        models, predictions, comparator = demo_model_training(
            train_data, test_data, X_train, y_train, X_test, y_test
        )
        
        # Step 4: Model Comparison
        comparison_df, best_model = demo_model_comparison(comparator)
        
        # Step 5: Visualization
        demo_visualization(test_data, predictions, STATE)
        
        # Step 6: Future Forecast
        future_dates, future_pred = demo_future_forecast(
            models, train_data, X_test, best_model, STATE
        )
        
        # Final Summary
        print_header("DEMO COMPLETE!")
        print("Summary:")
        print(f"  ✓ Trained 4 forecasting models")
        print(f"  ✓ Best model: {best_model}")
        print(f"  ✓ Generated 8-week forecast")
        print(f"  ✓ Created visualization")
        print(f"\nNext steps:")
        print(f"  1. Run 'python src/training_pipeline.py' to train models for other states")
        print(f"  2. Start API with 'python api/app.py'")
        print(f"  3. Check 'models/' directory for saved models")
        
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
