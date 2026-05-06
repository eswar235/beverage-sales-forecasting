# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Forecasting API is running"
}
```

---

### 2. Get Available States

Retrieve list of all available states in the dataset.

**Endpoint:** `GET /api/states`

**Response:**
```json
{
  "states": ["Alabama", "Arizona", "Arkansas", "California", ...],
  "count": 43
}
```

---

### 3. Get Available Models

Retrieve list of all available forecasting models.

**Endpoint:** `GET /api/models`

**Response:**
```json
{
  "models": ["ARIMA", "Prophet", "XGBoost", "LSTM"],
  "description": {
    "ARIMA": "Autoregressive Integrated Moving Average with seasonality",
    "Prophet": "Facebook Prophet for time series forecasting",
    "XGBoost": "Gradient Boosting with engineered features",
    "LSTM": "Long Short-Term Memory neural network"
  }
}
```

---

### 4. Generate Forecast

Generate sales forecast for a specific state using a chosen model.

**Endpoint:** `POST /api/forecast`

**Request Body:**
```json
{
  "state": "California",
  "model": "XGBoost",
  "steps": 8
}
```

**Parameters:**
- `state` (string, required): Name of the US state
- `model` (string, optional): Model name (ARIMA, Prophet, XGBoost, LSTM). Default: "XGBoost"
- `steps` (integer, optional): Number of weeks to forecast. Default: 8

**Response:**
```json
{
  "state": "California",
  "model": "XGBoost",
  "forecast": [
    {
      "date": "2023-01-08",
      "predicted_sales": 850000000.50
    },
    {
      "date": "2023-01-15",
      "predicted_sales": 860000000.75
    }
  ],
  "metadata": {
    "last_actual_date": "2023-01-01",
    "forecast_steps": 8
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid parameters
- `404 Not Found`: Model not trained for the specified state
- `500 Internal Server Error`: Server error

---

### 5. Get Historical Data

Retrieve historical sales data for a specific state.

**Endpoint:** `GET /api/historical`

**Query Parameters:**
- `state` (string, required): Name of the US state
- `limit` (integer, optional): Number of recent records to return. Default: 52

**Example:**
```
GET /api/historical?state=California&limit=52
```

**Response:**
```json
{
  "state": "California",
  "data": [
    {
      "date": "2022-01-02",
      "sales": 750000000.00
    },
    {
      "date": "2022-01-09",
      "sales": 760000000.00
    }
  ],
  "count": 52
}
```

---

### 6. Get Model Comparison

Retrieve performance comparison of all models for a specific state.

**Endpoint:** `GET /api/comparison`

**Query Parameters:**
- `state` (string, required): Name of the US state

**Example:**
```
GET /api/comparison?state=California
```

**Response:**
```json
{
  "state": "California",
  "comparison": {
    "XGBoost": {
      "MAE": 15234567.89,
      "RMSE": 18456789.12,
      "MAPE": 2.34,
      "R2": 0.95
    },
    "Prophet": {
      "MAE": 18345678.90,
      "RMSE": 21567890.23,
      "MAPE": 2.89,
      "R2": 0.93
    },
    "LSTM": {
      "MAE": 19456789.01,
      "RMSE": 23678901.34,
      "MAPE": 3.12,
      "R2": 0.91
    },
    "ARIMA": {
      "MAE": 22567890.12,
      "RMSE": 26789012.45,
      "MAPE": 3.67,
      "R2": 0.88
    }
  }
}
```

---

## Usage Examples

### Python

```python
import requests

# Base URL
base_url = "http://localhost:5000"

# 1. Health check
response = requests.get(f"{base_url}/health")
print(response.json())

# 2. Get states
response = requests.get(f"{base_url}/api/states")
states = response.json()['states']
print(f"Available states: {len(states)}")

# 3. Generate forecast
forecast_request = {
    "state": "California",
    "model": "XGBoost",
    "steps": 8
}
response = requests.post(f"{base_url}/api/forecast", json=forecast_request)
forecast = response.json()
print(f"Forecast for {forecast['state']}:")
for item in forecast['forecast']:
    print(f"  {item['date']}: ${item['predicted_sales']:,.2f}")

# 4. Get historical data
response = requests.get(f"{base_url}/api/historical", params={
    "state": "California",
    "limit": 10
})
historical = response.json()
print(f"Historical data points: {historical['count']}")

# 5. Get model comparison
response = requests.get(f"{base_url}/api/comparison", params={
    "state": "California"
})
comparison = response.json()
print("Model Performance:")
for model, metrics in comparison['comparison'].items():
    print(f"  {model}: RMSE = {metrics['RMSE']:,.2f}")
```

### JavaScript (Fetch API)

```javascript
const baseUrl = 'http://localhost:5000';

// 1. Health check
fetch(`${baseUrl}/health`)
  .then(response => response.json())
  .then(data => console.log(data));

// 2. Get states
fetch(`${baseUrl}/api/states`)
  .then(response => response.json())
  .then(data => console.log(`Available states: ${data.count}`));

// 3. Generate forecast
fetch(`${baseUrl}/api/forecast`, {
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
  .then(data => {
    console.log(`Forecast for ${data.state}:`);
    data.forecast.forEach(item => {
      console.log(`  ${item.date}: $${item.predicted_sales.toLocaleString()}`);
    });
  });

// 4. Get historical data
fetch(`${baseUrl}/api/historical?state=California&limit=10`)
  .then(response => response.json())
  .then(data => console.log(`Historical data points: ${data.count}`));

// 5. Get model comparison
fetch(`${baseUrl}/api/comparison?state=California`)
  .then(response => response.json())
  .then(data => {
    console.log('Model Performance:');
    Object.entries(data.comparison).forEach(([model, metrics]) => {
      console.log(`  ${model}: RMSE = ${metrics.RMSE.toLocaleString()}`);
    });
  });
```

### cURL

```bash
# 1. Health check
curl http://localhost:5000/health

# 2. Get states
curl http://localhost:5000/api/states

# 3. Generate forecast
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"state":"California","model":"XGBoost","steps":8}'

# 4. Get historical data
curl "http://localhost:5000/api/historical?state=California&limit=10"

# 5. Get model comparison
curl "http://localhost:5000/api/comparison?state=California"
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "error": "Error message description"
}
```

---

## Rate Limiting

Currently, there are no rate limits. For production use, consider implementing rate limiting.

---

## CORS

CORS is enabled for all origins. For production, configure specific allowed origins.

---

## Authentication

Currently, no authentication is required. For production use, implement API key or OAuth authentication.
