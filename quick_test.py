"""Quick test to verify the system works."""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from data_preprocessing import DataPreprocessor
        from feature_engineering import FeatureEngineer
        from model_comparison import ModelComparator
        from models.arima_model import ARIMAForecaster
        from models.prophet_model import ProphetForecaster
        from models.xgboost_model import XGBoostForecaster
        from models.lstm_model import LSTMForecaster
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_data_loading():
    """Test data loading."""
    print("\nTesting data loading...")
    try:
        from data_preprocessing import DataPreprocessor
        preprocessor = DataPreprocessor('data/beverage_sales.csv')
        preprocessor.load_data()
        print(f"✓ Loaded {len(preprocessor.df):,} records for {len(preprocessor.states)} states")
        return True
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False

def test_preprocessing():
    """Test preprocessing."""
    print("\nTesting preprocessing...")
    try:
        from data_preprocessing import DataPreprocessor
        preprocessor = DataPreprocessor('data/beverage_sales.csv')
        preprocessor.load_data()
        state_data = preprocessor.preprocess_state_data('California')
        print(f"✓ Preprocessed {len(state_data)} records for California")
        return True
    except Exception as e:
        print(f"✗ Preprocessing failed: {e}")
        return False

def test_feature_engineering():
    """Test feature engineering."""
    print("\nTesting feature engineering...")
    try:
        from data_preprocessing import DataPreprocessor
        from feature_engineering import FeatureEngineer
        
        preprocessor = DataPreprocessor('data/beverage_sales.csv')
        preprocessor.load_data()
        state_data = preprocessor.preprocess_state_data('California')
        
        engineer = FeatureEngineer()
        state_features = engineer.create_all_features(state_data)
        feature_cols = engineer.get_feature_columns(state_features)
        
        print(f"✓ Created {len(feature_cols)} features")
        return True
    except Exception as e:
        print(f"✗ Feature engineering failed: {e}")
        return False

def test_train_test_split():
    """Test train/test split."""
    print("\nTesting train/test split...")
    try:
        from data_preprocessing import DataPreprocessor
        
        preprocessor = DataPreprocessor('data/beverage_sales.csv')
        preprocessor.load_data()
        state_data = preprocessor.preprocess_state_data('California')
        train_data, test_data = preprocessor.get_train_test_split(state_data, test_weeks=8)
        
        print(f"✓ Train: {len(train_data)} records, Test: {len(test_data)} records")
        return True
    except Exception as e:
        print(f"✗ Train/test split failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 70)
    print("  QUICK SYSTEM TEST")
    print("=" * 70)
    
    tests = [
        test_imports,
        test_data_loading,
        test_preprocessing,
        test_feature_engineering,
        test_train_test_split
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 70)
    print("  TEST RESULTS")
    print("=" * 70)
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("\n✓ All tests passed! System is ready.")
        print("\nNext steps:")
        print("  1. Run demo: python demo.py")
        print("  2. Train models: python train_models.py California")
        print("  3. Start API: python api/app.py")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("  1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("  2. Check that data/beverage_sales.csv exists")
        print("  3. Verify Python version is 3.8 or higher")

if __name__ == "__main__":
    main()
