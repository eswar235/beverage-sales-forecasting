# Quick Start Guide

Get up and running with the Beverage Sales Forecasting System in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for LSTM)

## Installation

### Step 1: Navigate to Project Directory

```bash
cd forecasting_system
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- pandas, numpy (data processing)
- scikit-learn (ML utilities)
- xgboost (gradient boosting)
- tensorflow (deep learning)
- prophet (time series)
- statsmodels (ARIMA)
- flask (API)

**Note:** Installation may take 5-10 minutes depending on your internet connection.

## Quick Test

### Test 1: Train Models for California

Create a file `test_training.py`:

```python
from src.training_pipeline import ForecastingPipeline

# Train models for California
pipeline = ForecastingPipeline(
    data_path='data/beverage_sales.csv',
    state='California',
    test_weeks=8
)

pipeline.run()
```

Run it:
```bash
python test_training.py
```

**Expected Output:**
```
Loading and preprocessing data for California...
Loaded 43 records for 43 states
...
Training ARIMA Model
...
Training Prophet Model
...
Training XGBoost Model
...
Training LSTM Model
...
Model Comparison
...
Best Model: XGBoost
Pipeline Complete!
```

### Test 2: Start the API

```bash
cd api
python app.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
```

### Test 3: Make API Request

Open a new terminal and test:

```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Forecasting API is running"
}
```

## Your First Forecast

### Using Python

```python
import requests

# Generate 8-week forecast for California
response = requests.post('http://localhost:5000/api/forecast', json={
    'state': 'California',
    'model': 'XGBoost',
    'steps': 8
})

forecast = response.json()

# Print results
print(f"Forecast for {forecast['state']}:")
for item in forecast['forecast']:
    print(f"  {item['date']}: ${item['predicted_sales']:,.0f}")
```

### Using cURL

```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"state":"California","model":"XGBoost","steps":8}'
```

## Next Steps

### 1. Train Models for Other States

```python
from src.training_pipeline import ForecastingPipeline

states = ['Texas', 'Florida', 'New York']

for state in states:
    pipeline = ForecastingPipeline(
        data_path='data/beverage_sales.csv',
        state=state,
        test_weeks=8
    )
    pipeline.run()
```

### 2. Compare Model Performance

```python
import requests

response = requests.get('http://localhost:5000/api/comparison', 
                       params={'state': 'California'})
comparison = response.json()

print("Model Performance (RMSE):")
for model, metrics in comparison['comparison'].items():
    print(f"  {model}: {metrics['RMSE']:,.0f}")
```

### 3. Visualize Results

```python
import matplotlib.pyplot as plt
import requests

# Get historical data
hist_response = requests.get('http://localhost:5000/api/historical',
                            params={'state': 'California', 'limit': 20})
historical = hist_response.json()['data']

# Get forecast
forecast_response = requests.post('http://localhost:5000/api/forecast',
                                 json={'state': 'California', 'steps': 8})
forecast = forecast_response.json()['forecast']

# Plot
hist_dates = [item['date'] for item in historical]
hist_sales = [item['sales'] for item in historical]
fore_dates = [item['date'] for item in forecast]
fore_sales = [item['predicted_sales'] for item in forecast]

plt.figure(figsize=(12, 6))
plt.plot(hist_dates, hist_sales, label='Historical', marker='o')
plt.plot(fore_dates, fore_sales, label='Forecast', marker='s', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.title('California Beverage Sales Forecast')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Common Issues

### Issue 1: Import Errors

**Problem:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: Memory Error with LSTM

**Problem:** `MemoryError` when training LSTM

**Solution:** Reduce batch size or epochs:
```python
lstm.train(train_data, epochs=30, batch_size=8)
```

### Issue 3: Port Already in Use

**Problem:** `Address already in use`

**Solution:** Use a different port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue 4: Prophet Warnings

**Problem:** Multiple warnings from Prophet

**Solution:** These are normal and can be ignored. To suppress:
```python
import warnings
warnings.filterwarnings('ignore')
```

## Performance Tips

1. **Start with XGBoost**: Fastest and often most accurate
2. **Skip LSTM for quick tests**: Takes longest to train
3. **Use smaller test_weeks**: Faster evaluation (e.g., test_weeks=4)
4. **Train one state first**: Verify everything works before batch processing

## What's Next?

- Read the full [README.md](../README.md) for detailed documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for all API endpoints
- Explore individual model implementations in `src/models/`
- Customize hyperparameters for better performance

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Verify all dependencies are installed
3. Ensure the dataset file exists at `data/beverage_sales.csv`
4. Check Python version (3.8+)

Happy forecasting! 🚀
