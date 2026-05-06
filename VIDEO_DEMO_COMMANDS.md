# 🎥 Video Demo - Simple Command List

## 🎬 Just Copy & Run These Commands in Order

---

### 1️⃣ Check Data (30 seconds)
```bash
python check_data.py
```

---

### 2️⃣ Quick Test (30 seconds)
```bash
python quick_test.py
```

---

### 3️⃣ Main Demo - Train Models (3 minutes) ⭐
```bash
python demo.py
```

---

### 4️⃣ Show Visualization
```bash
start models\California_forecast_comparison.png
```

---

### 5️⃣ Train More States (1 minute)
```bash
python train_models.py Texas Florida
```

---

### 6️⃣ Start API Server
```bash
python api/app.py
```
**Wait for:** `Running on http://127.0.0.1:5000`

---

### 7️⃣ Test API - EASY METHOD! 🎯

**Open the test page in your browser:**
```bash
start test_api.html
```

Then click the buttons to test each endpoint! Much easier for video! ✅

**Alternative - Command Line (if you prefer):**
```powershell
curl.exe http://localhost:5000/health
curl.exe http://localhost:5000/api/states
curl.exe http://localhost:5000/api/models
```

---

## ✅ Done! That's it!

**Total Time:** ~10 minutes

**Key Results to Mention:**
- 8,944 records, 43 states
- 19 features created
- XGBoost won: R² = 0.61, MAPE = 2.44%
- Full REST API working
