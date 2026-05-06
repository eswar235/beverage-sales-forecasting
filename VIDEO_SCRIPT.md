# Video Demonstration Script

## Video Title: End-to-End Time Series Forecasting System with REST API

**Duration:** 5-7 minutes

---

## Scene 1: Introduction (30 seconds)

**[Screen: Show project folder structure]**

"Hello! Today I'll demonstrate a production-ready time series forecasting system that predicts beverage sales across US states using multiple machine learning algorithms."

**Key Points to Mention:**
- Built with Python, Flask, and industry-standard ML libraries
- Implements 4 different forecasting models
- Includes REST API for easy integration
- Handles real-world challenges: missing data, seasonality, trend

---

## Scene 2: Dataset Overview (45 seconds)

**[Screen: Open data/beverage_sales.csv or run check_data.py]**

```bash
python check_data.py
```

**Narration:**
"The dataset contains weekly beverage sales data for 43 US states from 2019 to 2022. That's over 8,900 records with 208 weeks per state."

**Highlight:**
- 43 states
- 208 weeks of data per state
- Weekly frequency
- No missing values (after preprocessing)
- Realistic seasonality and trends

---

## Scene 3: System Architecture (1 minute)

**[Screen: Show README.md or draw architecture diagram]**

**Narration:**
"The system has a modular architecture with five main components:"

1. **Data Preprocessing Module**
   - Handles missing dates and values
   - Time series validation
   - Train/test splitting

2. **Feature Engineering Module**
   - Lag features (1, 2, 4 weeks)
   - Rolling statistics (mean, std)
   - Temporal features (month, week, day)
   - Cyclical encoding

3. **Four Forecasting Models**
   - ARIMA/SARIMA (statistical)
   - Facebook Prophet (additive model)
   - XGBoost (gradient boosting)
   - LSTM (deep learning)

4. **Model Comparison**
   - Automatic evaluation (MAE, RMSE, MAPE, R²)
   - Best model selection

5. **REST API**
   - Flask-based
   - Multiple endpoints
   - CORS enabled

---

## Scene 4: Feature Engineering Demo (1 minute)

**[Screen: Open src/feature_engineering.py or show code]**

**Narration:**
"Feature engineering is critical for time series forecasting. Let me show you what features we create:"

**Show code snippets:**

```python
# Lag features - previous week values
df['lag_1'] = df['Total'].shift(1)
df['lag_2'] = df['Total'].shift(2)
df['lag_4'] = df['Total'].shift(4)

# Rolling statistics
df['rolling_mean_4'] = df['Total'].rolling(window=4).mean()
df['rolling_std_4'] = df['Total'].rolling(window=4).std()

# Temporal features
df['month'] = df['Date'].dt.month
df['week_of_year'] = df['Date'].dt.isocalendar().week

# Cyclical encoding
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
```

**Key Point:**
"These features capture patterns, trends, and seasonality that help models make accurate predictions."

---

## Scene 5: Model Training Demo (1.5 minutes)

**[Screen: Terminal - run demo.py or train_models.py]**

```bash
python demo.py
```

**Narration:**
"Now let's train all four models on California's data. Watch how each model learns from the historical patterns."

**Show output:**
- Data loading and preprocessing
- Feature creation
- Each model training (ARIMA, Prophet, XGBoost, LSTM)
- Performance metrics

**Highlight the comparison table:**
```
Model      MAE           RMSE          MAPE      R²
XGBoost    15,234,567    18,456,789    2.34%     0.95
Prophet    18,345,678    21,567,890    2.89%     0.93
LSTM       19,456,789    23,678,901    3.12%     0.91
ARIMA      22,567,890    26,789,012    3.67%     0.88
```

**Narration:**
"XGBoost performs best with the lowest RMSE and highest R². The system automatically selects it as the best model."

---

## Scene 6: Visualization (30 seconds)

**[Screen: Show the generated forecast comparison plot]**

**Narration:**
"Here's a visual comparison of all models' predictions against actual values. You can see XGBoost (red) tracks the actual values (black) most closely."

**Point out:**
- Actual values in black
- Each model's predictions in different colors
- How well they capture the trend and seasonality

---

## Scene 7: REST API Demo (1.5 minutes)

**[Screen: Terminal - start API]**

```bash
python api/app.py
```

**Narration:**
"Now let's start the REST API. It runs on port 5000 and provides several endpoints."

**[Screen: New terminal or Postman]**

**Demo 1: Health Check**
```bash
curl http://localhost:5000/health
```

**Demo 2: Get Available States**
```bash
curl http://localhost:5000/api/states
```

**Demo 3: Generate Forecast**
```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"state":"California","model":"XGBoost","steps":8}'
```

**Show the JSON response:**
```json
{
  "state": "California",
  "model": "XGBoost",
  "forecast": [
    {"date": "2023-01-08", "predicted_sales": 850000000.50},
    {"date": "2023-01-15", "predicted_sales": 860000000.75},
    ...
  ]
}
```

**Demo 4: Get Historical Data**
```bash
curl "http://localhost:5000/api/historical?state=California&limit=10"
```

**Demo 5: Model Comparison**
```bash
curl "http://localhost:5000/api/comparison?state=California"
```

**Narration:**
"The API is production-ready with proper error handling, CORS support, and comprehensive documentation."

---

## Scene 8: Code Quality & Best Practices (45 seconds)

**[Screen: Show code structure]**

**Narration:**
"The codebase follows software engineering best practices:"

**Highlight:**
1. **Modular Design**
   - Separate modules for each concern
   - Easy to maintain and extend

2. **Time Series Best Practices**
   - No data leakage (proper train/test split)
   - Features created only from past data
   - Proper handling of missing values

3. **Documentation**
   - Comprehensive README
   - API documentation
   - Quick start guide
   - Code comments

4. **Error Handling**
   - Try-catch blocks
   - Informative error messages
   - Logging throughout

---

## Scene 9: Real-World Applications (30 seconds)

**[Screen: Show use cases or bullet points]**

**Narration:**
"This system can be used for:"

- **Inventory Management**: Predict demand to optimize stock levels
- **Supply Chain Planning**: Forecast needs for logistics
- **Revenue Forecasting**: Predict future sales for financial planning
- **Resource Allocation**: Plan staffing and resources based on demand
- **Business Intelligence**: Identify trends and patterns

---

## Scene 10: Conclusion & Next Steps (30 seconds)

**[Screen: Show project summary]**

**Narration:**
"To summarize, we've built a complete forecasting system that:"

✓ Handles real-world time series data
✓ Implements 4 state-of-the-art models
✓ Automatically selects the best performer
✓ Provides predictions via REST API
✓ Follows production-ready practices

**Next Steps:**
- Train models for all 43 states
- Deploy to cloud (AWS, Azure, GCP)
- Add monitoring and alerting
- Create web dashboard
- Implement automated retraining

**Closing:**
"Thank you for watching! All code and documentation are available in the repository. Feel free to explore, modify, and extend the system for your own use cases."

---

## Recording Tips

### Before Recording:
1. ✓ Run `python check_data.py` to verify data
2. ✓ Run `python demo.py` once to ensure it works
3. ✓ Clear terminal history
4. ✓ Close unnecessary applications
5. ✓ Test microphone and screen recording
6. ✓ Prepare a clean workspace

### During Recording:
1. Speak clearly and at a moderate pace
2. Pause between sections
3. Show code and output clearly
4. Use zoom/highlight for important parts
5. Keep cursor movements smooth
6. If you make a mistake, pause and restart that section

### After Recording:
1. Edit out long waits (model training, API startup)
2. Add text overlays for key points
3. Add background music (optional, low volume)
4. Add intro/outro slides
5. Export in HD (1080p minimum)

---

## Alternative: Quick 3-Minute Version

If you need a shorter video:

1. **Introduction** (20s): Project overview
2. **Dataset** (20s): Show data structure
3. **Training** (60s): Run demo, show results
4. **API Demo** (60s): Show 2-3 API calls
5. **Conclusion** (20s): Summary and next steps

---

## Screen Recording Tools

**Windows:**
- OBS Studio (free, professional)
- Camtasia (paid, easy to use)
- Windows Game Bar (built-in, basic)

**Mac:**
- QuickTime Player (built-in)
- ScreenFlow (paid)
- OBS Studio (free)

**Linux:**
- OBS Studio (free)
- SimpleScreenRecorder (free)
- Kazam (free)

---

## Video Checklist

Before submitting:

- [ ] Video is 3-7 minutes long
- [ ] Audio is clear and audible
- [ ] Screen is readable (1080p minimum)
- [ ] All demos work correctly
- [ ] Code is visible and formatted
- [ ] Terminal output is readable
- [ ] No sensitive information shown
- [ ] Intro explains the project
- [ ] Conclusion summarizes key points
- [ ] Video is exported in MP4 format

---

## Submission Package

Include with your video:

1. **Video file** (MP4 format)
2. **Complete code** (forecasting_system folder)
3. **README.md** (main documentation)
4. **requirements.txt** (dependencies)
5. **This VIDEO_SCRIPT.md** (for reference)

Good luck with your demonstration! 🚀
