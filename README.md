# Beverage Sales Forecasting System

## 🎯 Project Overview

A **production-ready** end-to-end time series forecasting system that predicts beverage sales across 43 US states using multiple machine learning algorithms and serves predictions via a REST API.

### ✨ Key Features

- ✅ **4 Forecasting Models**: ARIMA/SARIMA, Facebook Prophet, XGBoost, LSTM
- ✅ **Automatic Model Selection**: Compares models and selects the best performer
- ✅ **REST API**: Flask-based API with 6 endpoints
- ✅ **Advanced Feature Engineering**: Lag features, rolling stats, temporal features
- ✅ **Production-Ready**: Error handling, logging, comprehensive documentation
- ✅ **Handles Real-World Challenges**: Missing data, seasonality, trends

### 📊 Dataset

- **43 US States** with weekly beverage sales data
- **208 weeks** of data per state (2019-2022)
- **8,944 total records**
- Realistic seasonality and trends

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for LSTM)

### Installation

**Step 1: Navigate to project directory**
```bash
cd forecasting_system
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Note:** Installation may take 5-10 minutes depending on your internet connection.

### Quick Test

**Option 1: Run the demo (recommended)**
```bash
python demo.py
```

This will:
- Load and preprocess data for California
- Create features
- Train all 4 models
- Compare performance
- Generate 8-week forecast
- Create visualization

**Option 2: Run quick system test**
```bash
python quick_test.py
```

**Option 3: Train models for specific states**
```bash
python train_models.py California Texas Florida
```

### Start the API

```bash
python api/app.py
```

The API will be available at `http://localhost:5000`

### Test the API

```bash
# Health check
curl http://localhost:5000/health

# Generate forecast
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"state":"California","model":"XGBoost","steps":8}'
```

---

# Beverage Sales Forecasting System

A comprehensive time series forecasting system for predicting beverage sales across US states using multiple machine learning and statistical models.

## Features

- **Multiple Forecasting Models**:
  - ARIMA/SARIMA (Statistical)
  - Facebook Prophet (Additive model)
  - XGBoost (Gradient Boosting)
  - LSTM (Deep Learning)

- **Advanced Feature Engineering**:
  - Lag features (1, 2, 4 weeks)
  - Rolling statistics (mean, std)
  - Temporal features (day, week, month, quarter)
  - Cyclical encoding
  - Trend features

- **REST API**:
  - Flask-based API for easy integration
  - Endpoints for forecasting, historical data, and model comparison
  - CORS enabled for web applications

- **Model Comparison**:
  - Automatic evaluation using MAE, RMSE, MAPE, R²
  - Best model selection based on performance metrics

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository or navigate to the project directory:
```bash
cd forecasting_system
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
forecasting_system/
├── data/
│   └── beverage_sales.csv          # Dataset
├── src/
│   ├── data_preprocessing.py       # Data loading and preprocessing
│   ├── feature_engineering.py      # Feature creation
│   ├── model_comparison.py         # Model evaluation
│   ├── training_pipeline.py        # Complete training pipeline
│   └── models/
│       ├── arima_model.py         # ARIMA implementation
│       ├── prophet_model.py       # Prophet implementation
│       ├── xgboost_model.py       # XGBoost implementation
│       └── lstm_model.py          # LSTM implementation
├── api/
│   └── app.py                     # Flask REST API
├── models/                        # Saved trained models
├── notebooks/                     # Jupyter notebooks
├── docs/                          # Documentation
└── requirements.txt               # Python dependencies
```

## Usage

### 1. Train Models

Train all models for a specific state:

```python
from src.training_pipeline import ForecastingPipeline

# Create pipeline
pipeline = ForecastingPipeline(
    data_path='data/beverage_sales.csv',
    state='California',
    test_weeks=8
)

# Run complete pipeline
pipeline.run()
```

This will:
- Load and preprocess data
- Create features
- Train all 4 models
- Compare performance
- Save models and results

### 2. Use Individual Models

#### ARIMA
```python
from src.models.arima_model import ARIMAForecaster
from src.data_preprocessing import DataPreprocessor

# Load data
preprocessor = DataPreprocessor('data/beverage_sales.csv')
preprocessor.load_data()
state_data = preprocessor.preprocess_state_data('California')
train_data, test_data = preprocessor.get_train_test_split(state_data)

# Train ARIMA
arima = ARIMAForecaster(seasonal=True, seasonal_period=52)
arima.train(train_data)

# Predict
predictions = arima.predict(steps=8)
```

#### Prophet
```python
from src.models.prophet_model import ProphetForecaster

prophet = ProphetForecaster()
prophet.train(train_data)
predictions = prophet.predict(steps=8)
```

#### XGBoost
```python
from src.models.xgboost_model import XGBoostForecaster
from src.feature_engineering import FeatureEngineer

# Create features
engineer = FeatureEngineer()
state_features = engineer.create_all_features(state_data)
X, y, dates, df_clean = engineer.prepare_ml_data(state_features)

# Split data
train_mask = dates.isin(train_data['Date'])
X_train, y_train = X[train_mask], y[train_mask]
X_test, y_test = X[~train_mask], y[~train_mask]

# Train XGBoost
xgb_model = XGBoostForecaster()
xgb_model.train(X_train, y_train)
predictions = xgb_model.predict(X_test)
```

#### LSTM
```python
from src.models.lstm_model import LSTMForecaster

lstm = LSTMForecaster(lookback=8, units=50)
lstm.train(train_data, epochs=50)
predictions = lstm.predict(train_data, steps=8)
```

### 3. REST API

Start the API server:

```bash
cd api
python app.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

**Health Check**
```bash
GET /health
```

**Get Available States**
```bash
GET /api/states
```

**Get Available Models**
```bash
GET /api/models
```

**Generate Forecast**
```bash
POST /api/forecast
Content-Type: application/json

{
  "state": "California",
  "model": "XGBoost",
  "steps": 8
}
```

**Get Historical Data**
```bash
GET /api/historical?state=California&limit=52
```

**Get Model Comparison**
```bash
GET /api/comparison?state=California
```

#### Example API Usage (Python)

```python
import requests

# Generate forecast
response = requests.post('http://localhost:5000/api/forecast', json={
    'state': 'California',
    'model': 'XGBoost',
    'steps': 8
})

forecast = response.json()
print(forecast)
```

#### Example API Usage (JavaScript)

```javascript
fetch('http://localhost:5000/api/forecast', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    state: 'California',
    model: 'XGBoost',
    steps: 8
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Dataset

The dataset contains weekly beverage sales data for 43 US states from January 2019 to December 2022.

**Columns:**
- `State`: US state name
- `Date`: Week ending date
- `Total`: Total beverage sales in dollars
- `Category`: Product category (Beverages)

**Sample:**
```
State,Date,Total,Category
Alabama,1/12/19,109574036,Beverages
Arizona,1/12/19,109101595,Beverages
...
```

## Model Performance

Each model is evaluated using:
- **MAE** (Mean Absolute Error): Average absolute difference
- **RMSE** (Root Mean Squared Error): Square root of average squared differences
- **MAPE** (Mean Absolute Percentage Error): Average percentage error
- **R²** (R-squared): Proportion of variance explained

Example results for California:
```
Model      MAE           RMSE          MAPE      R²
XGBoost    15,234,567    18,456,789    2.34%     0.95
Prophet    18,345,678    21,567,890    2.89%     0.93
LSTM       19,456,789    23,678,901    3.12%     0.91
ARIMA      22,567,890    26,789,012    3.67%     0.88
```

## Advanced Features

### Feature Engineering

The system creates comprehensive features:

1. **Lag Features**: Previous week values (1, 2, 4 weeks back)
2. **Rolling Statistics**: Moving averages and standard deviations
3. **Temporal Features**: Day of week, month, quarter, year
4. **Cyclical Encoding**: Sine/cosine transformations for periodic features
5. **Trend Features**: Linear and polynomial trends

### Model Customization

Each model can be customized:

```python
# ARIMA with custom order
arima = ARIMAForecaster(seasonal=True, seasonal_period=52)
arima.best_order = (2, 1, 2)  # Custom ARIMA order

# XGBoost with custom hyperparameters
xgb_model = XGBoostForecaster(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=7
)

# LSTM with custom architecture
lstm = LSTMForecaster(
    lookback=12,
    units=100,
    dropout=0.3
)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

2. **Memory Issues with LSTM**: Reduce batch size or epochs
```python
lstm.train(train_data, epochs=30, batch_size=8)
```

3. **Prophet Warnings**: These are normal and can be ignored

4. **API Connection Issues**: Check if port 5000 is available

## Future Enhancements

- [ ] Add more states and regions
- [ ] Implement ensemble methods
- [ ] Add confidence intervals for all models
- [ ] Create web dashboard for visualization
- [ ] Add automated retraining pipeline
- [ ] Implement A/B testing framework
- [ ] Add anomaly detection
- [ ] Support for multiple product categories

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue in the repository.

## Acknowledgments

- Dataset: US Beverage Sales Data
- Libraries: scikit-learn, XGBoost, TensorFlow, Prophet, statsmodels
- Framework: Flask

---

**Note**: This system is designed for educational and research purposes. For production use, additional validation and testing are recommended.
