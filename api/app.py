"""Flask REST API for beverage sales forecasting."""
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer

app = Flask(__name__)
CORS(app)

# Global variables
MODELS_DIR = Path(__file__).parent.parent / 'models'
DATA_PATH = Path(__file__).parent.parent / 'data' / 'beverage_sales.csv'
loaded_models = {}


def load_model(state, model_name):
    """Load a trained model."""
    key = f"{state}_{model_name}"
    
    if key not in loaded_models:
        model_file = MODELS_DIR / f"{key}.pkl"
        
        if not model_file.exists():
            return None
        
        with open(model_file, 'rb') as f:
            loaded_models[key] = pickle.load(f)
    
    return loaded_models[key]


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Forecasting API is running'
    })


@app.route('/api/states', methods=['GET'])
def get_states():
    """Get list of available states."""
    try:
        preprocessor = DataPreprocessor(str(DATA_PATH))
        preprocessor.load_data()
        
        states = preprocessor.states.tolist()
        
        return jsonify({
            'states': states,
            'count': len(states)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available models."""
    return jsonify({
        'models': ['ARIMA', 'Prophet', 'XGBoost', 'LSTM'],
        'description': {
            'ARIMA': 'Autoregressive Integrated Moving Average with seasonality',
            'Prophet': 'Facebook Prophet for time series forecasting',
            'XGBoost': 'Gradient Boosting with engineered features',
            'LSTM': 'Long Short-Term Memory neural network'
        }
    })


@app.route('/api/forecast', methods=['POST'])
def forecast():
    """
    Generate forecast for a state using specified model.
    
    Request body:
    {
        "state": "California",
        "model": "XGBoost",
        "steps": 8
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        state = data.get('state')
        model_name = data.get('model', 'XGBoost')
        steps = data.get('steps', 8)
        
        if not state:
            return jsonify({'error': 'State is required'}), 400
        
        if model_name not in ['ARIMA', 'Prophet', 'XGBoost', 'LSTM']:
            return jsonify({'error': 'Invalid model name'}), 400
        
        # Load model
        model = load_model(state, model_name)
        
        if model is None:
            return jsonify({
                'error': f'Model not found for {state}. Please train the model first.'
            }), 404
        
        # Load and preprocess data
        preprocessor = DataPreprocessor(str(DATA_PATH))
        preprocessor.load_data()
        state_data = preprocessor.preprocess_state_data(state)
        
        # Generate predictions based on model type
        if model_name in ['ARIMA', 'Prophet']:
            predictions = model.predict(steps=steps)
        
        elif model_name == 'LSTM':
            predictions = model.predict(state_data, steps=steps)
        
        elif model_name == 'XGBoost':
            # For XGBoost, we need features
            engineer = FeatureEngineer()
            state_features = engineer.create_all_features(state_data)
            X, y, dates, df_clean = engineer.prepare_ml_data(state_features)
            
            # Use last available features for prediction
            X_last = X.tail(steps)
            predictions = model.predict(X_last)
        
        # Create forecast dates
        last_date = state_data['Date'].max()
        forecast_dates = pd.date_range(
            start=last_date + pd.Timedelta(weeks=1),
            periods=steps,
            freq='W'
        )
        
        # Prepare response
        forecast_data = []
        for date, value in zip(forecast_dates, predictions):
            forecast_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'predicted_sales': float(value)
            })
        
        return jsonify({
            'state': state,
            'model': model_name,
            'forecast': forecast_data,
            'metadata': {
                'last_actual_date': last_date.strftime('%Y-%m-%d'),
                'forecast_steps': steps
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/historical', methods=['GET'])
def get_historical():
    """
    Get historical data for a state.
    
    Query parameters:
    - state: State name (required)
    - limit: Number of recent records (optional, default: 52)
    """
    try:
        state = request.args.get('state')
        limit = int(request.args.get('limit', 52))
        
        if not state:
            return jsonify({'error': 'State parameter is required'}), 400
        
        # Load data
        preprocessor = DataPreprocessor(str(DATA_PATH))
        preprocessor.load_data()
        state_data = preprocessor.preprocess_state_data(state)
        
        # Get recent data
        recent_data = state_data.tail(limit)
        
        # Prepare response
        historical_data = []
        for _, row in recent_data.iterrows():
            historical_data.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'sales': float(row['Total'])
            })
        
        return jsonify({
            'state': state,
            'data': historical_data,
            'count': len(historical_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/comparison', methods=['GET'])
def get_comparison():
    """
    Get model comparison results for a state.
    
    Query parameters:
    - state: State name (required)
    """
    try:
        state = request.args.get('state')
        
        if not state:
            return jsonify({'error': 'State parameter is required'}), 400
        
        # Load comparison results
        comparison_file = MODELS_DIR / f"{state}_comparison.csv"
        
        if not comparison_file.exists():
            return jsonify({
                'error': f'Comparison results not found for {state}'
            }), 404
        
        comparison_df = pd.read_csv(comparison_file, index_col=0)
        
        # Convert to dict
        comparison_data = comparison_df.to_dict('index')
        
        return jsonify({
            'state': state,
            'comparison': comparison_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
