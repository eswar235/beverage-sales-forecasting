# 🔧 Technical Guide

Complete technical documentation for the Beverage Sales Forecasting System.

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Pipeline](#data-pipeline)
3. [Feature Engineering](#feature-engineering)
4. [Models](#models)
5. [API Design](#api-design)
6. [Performance Optimization](#performance-optimization)
7. [Deployment](#deployment)

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CSV Data   │ -> │ Preprocessor │ -> │  Clean Data  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Feature Engineering                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Lag    │  │ Rolling  │  │ Temporal │  │  Trend   │   │
│  │ Features │  │   Stats  │  │ Features │  │ Features │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Model Layer                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  ARIMA   │  │ Prophet  │  │ XGBoost  │  │   LSTM   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Model Comparison                            │
│              Select Best Model (RMSE)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      REST API                                │
│  Flask Server with 6 Endpoints + CORS                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Pipeline

### 1. Data Loading

**File:** `src/data_preprocessing.py`

```python
class DataPreprocessor:
    def load_data(self):
        # Load CSV
        # Convert dates
        # Sort by state and date
        # Validate data
```

**Input:** CSV file with columns: State, Date, Total, Category  
**Output:** Pandas DataFrame with datetime index

### 2. Data Preprocessing

**Steps:**
1. **Date Parsing:** Convert string dates to datetime
2. **Missing Dates:** Fill gaps in weekly data
3. **Missing Values:** Interpolate using forward fill + linear interpolation
4. **Validation:** Check for duplicates and outliers

**Key Functions:**
- `handle_missing_dates()` - Ensures complete date range
- `handle_missing_values()` - Imputes missing values
- `preprocess_state_data()` - Complete pipeline for one state

### 3. Train/Test Split

**Method:** Time-based split (not random)
- **Train:** First N-8 weeks
- **Test:** Last 8 weeks

**Rationale:** Preserves temporal order for time series

---

## 🔧 Feature Engineering

**File:** `src/feature_engineering.py`

### Feature Categories

#### 1. Lag Features
```python
lag_1 = df['Total'].shift(1)  # Previous week
lag_2 = df['Total'].shift(2)  # 2 weeks ago
lag_4 = df['Total'].shift(4)  # 4 weeks ago
```

**Purpose:** Capture autocorrelation

#### 2. Rolling Statistics
```python
rolling_mean_4 = df['Total'].rolling(4).mean()
rolling_std_4 = df['Total'].rolling(4).std()
rolling_mean_8 = df['Total'].rolling(8).mean()
rolling_std_8 = df['Total'].rolling(8).std()
```

**Purpose:** Capture trends and volatility

#### 3. Temporal Features
```python
day_of_week = df['Date'].dt.dayofweek
month = df['Date'].dt.month
quarter = df['Date'].dt.quarter
week_of_year = df['Date'].dt.isocalendar().week
```

**Purpose:** Capture seasonality

#### 4. Cyclical Encoding
```python
month_sin = np.sin(2 * np.pi * month / 12)
month_cos = np.cos(2 * np.pi * month / 12)
```

**Purpose:** Preserve cyclical nature of time

#### 5. Trend Features
```python
trend = np.arange(len(df))
trend_squared = trend ** 2
```

**Purpose:** Capture long-term trends

### Feature Importance (XGBoost)

| Feature | Importance |
|---------|-----------|
| rolling_mean_4 | 44.3% |
| month_sin | 27.4% |
| week_of_year | 10.1% |
| rolling_std_4 | 2.9% |
| month | 2.7% |

---

## 🤖 Models

### 1. ARIMA/SARIMA

**File:** `src/models/arima_model.py`

**Algorithm:** Autoregressive Integrated Moving Average with Seasonality

**Parameters:**
- Order: (p, d, q) = (1, 1, 1)
- Seasonal Order: (P, D, Q, s) = (1, 1, 1, 52)
- Seasonal Period: 52 weeks

**Strengths:**
- ✅ Good for stable patterns
- ✅ Handles seasonality
- ✅ Interpretable

**Weaknesses:**
- ❌ Assumes linear relationships
- ❌ Sensitive to outliers

**Performance (California):**
- MAE: $13.6M
- RMSE: $17.6M
- MAPE: 3.18%
- R²: 0.46

---

### 2. Facebook Prophet

**File:** `src/models/prophet_model.py`

**Algorithm:** Additive model with trend, seasonality, and holidays

**Components:**
- Trend: Piecewise linear or logistic
- Seasonality: Fourier series
- Holidays: Optional (not used)

**Strengths:**
- ✅ Handles missing data
- ✅ Robust to outliers
- ✅ Easy to use

**Weaknesses:**
- ❌ Less accurate for complex patterns
- ❌ Limited customization

**Performance (California):**
- MAE: $18.4M
- RMSE: $24.1M
- MAPE: 4.44%
- R²: -0.01

---

### 3. XGBoost (Best Model 🏆)

**File:** `src/models/xgboost_model.py`

**Algorithm:** Gradient Boosting with Decision Trees

**Hyperparameters:**
```python
n_estimators = 100
learning_rate = 0.1
max_depth = 5
min_child_weight = 1
subsample = 0.8
colsample_bytree = 0.8
```

**Strengths:**
- ✅ Handles non-linear relationships
- ✅ Feature importance
- ✅ Fast training
- ✅ Best performance

**Weaknesses:**
- ❌ Requires feature engineering
- ❌ Less interpretable

**Performance (California):**
- MAE: $10.2M
- RMSE: $15.0M
- MAPE: 2.44%
- R²: 0.61

---

### 4. LSTM

**File:** `src/models/lstm_model.py`

**Algorithm:** Long Short-Term Memory Neural Network

**Architecture:**
```python
LSTM(units=50, return_sequences=True)
Dropout(0.2)
LSTM(units=50)
Dropout(0.2)
Dense(1)
```

**Strengths:**
- ✅ Captures long-term dependencies
- ✅ Handles complex patterns

**Weaknesses:**
- ❌ Requires TensorFlow
- ❌ Slow training
- ❌ Needs more data

**Status:** Optional (TensorFlow dependency)

---

## 🌐 API Design

**File:** `api/app.py`

### Architecture

**Framework:** Flask  
**CORS:** Enabled for web applications  
**Port:** 5000  
**Host:** 0.0.0.0 (all interfaces)

### Endpoints

#### 1. Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "Forecasting API is running"
}
```

#### 2. Get States
```
GET /api/states
```
**Response:**
```json
{
  "states": ["Alabama", "Arizona", ...],
  "count": 43
}
```

#### 3. Get Models
```
GET /api/models
```
**Response:**
```json
{
  "models": ["ARIMA", "Prophet", "XGBoost", "LSTM"],
  "description": {...}
}
```

#### 4. Generate Forecast
```
POST /api/forecast
Content-Type: application/json

{
  "state": "California",
  "model": "XGBoost",
  "steps": 8
}
```

**Response:**
```json
{
  "state": "California",
  "model": "XGBoost",
  "forecast": [
    {"date": "2023-01-01", "predicted_sales": 454966560},
    ...
  ],
  "metadata": {
    "last_actual_date": "2022-12-31",
    "forecast_steps": 8
  }
}
```

#### 5. Historical Data
```
GET /api/historical?state=California&limit=52
```

#### 6. Model Comparison
```
GET /api/comparison?state=California
```

### Error Handling

**400 Bad Request:** Invalid input  
**404 Not Found:** Model or state not found  
**500 Internal Server Error:** Server error

---

## ⚡ Performance Optimization

### 1. Model Caching
```python
loaded_models = {}  # Cache loaded models
```

### 2. Data Preprocessing
- Vectorized operations with NumPy
- Efficient pandas operations
- Minimal data copying

### 3. Feature Engineering
- Batch processing
- Reuse computed features

### 4. API Optimization
- CORS enabled
- JSON compression
- Efficient serialization

---

## 🚀 Deployment

### Local Development
```bash
python api/app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api.app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api.app:app"]
```

### Cloud Deployment

**Options:**
- AWS EC2 + Elastic Beanstalk
- Google Cloud Run
- Azure App Service
- Heroku

**Requirements:**
- Python 3.8+
- 2GB RAM minimum
- 10GB storage

---

## 📈 Monitoring

### Metrics to Track
- API response time
- Model prediction accuracy
- Error rates
- Resource usage

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

---

## 🔒 Security

### Best Practices
- ✅ Input validation
- ✅ Error handling
- ✅ CORS configuration
- ✅ Rate limiting (recommended)
- ✅ Authentication (recommended for production)

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
python quick_test.py
```

### API Tests
```bash
# Use test_api.html
# Or curl commands
```

---

## 📚 References

### Libraries Used
- pandas: Data manipulation
- numpy: Numerical operations
- scikit-learn: ML utilities
- xgboost: Gradient boosting
- statsmodels: ARIMA
- prophet: Facebook Prophet
- tensorflow: LSTM (optional)
- flask: REST API

### Papers & Resources
- XGBoost: Chen & Guestrin (2016)
- Prophet: Taylor & Letham (2018)
- ARIMA: Box & Jenkins (1970)
- LSTM: Hochreiter & Schmidhuber (1997)

---

**Last Updated:** May 6, 2026  
**Version:** 1.0.0
