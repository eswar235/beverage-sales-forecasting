# Installation Guide

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum
- **Disk Space**: 2GB free space
- **Internet**: Required for package installation

### Recommended Requirements
- **RAM**: 8GB or more (for LSTM training)
- **CPU**: Multi-core processor
- **Python**: 3.9 or 3.10

---

## Step-by-Step Installation

### Step 1: Verify Python Installation

**Check Python version:**
```bash
python --version
```

**Expected output:** `Python 3.8.x` or higher

**If Python is not installed:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3` or download from python.org
- **Linux**: `sudo apt-get install python3 python3-pip`

### Step 2: Navigate to Project Directory

```bash
cd forecasting_system
```

### Step 3: Create Virtual Environment (Recommended)

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Easy to manage and clean up

**Create virtual environment:**

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

**You should see `(venv)` in your terminal prompt.**

### Step 4: Upgrade pip (Optional but Recommended)

```bash
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**This will install:**
- pandas (data manipulation)
- numpy (numerical computing)
- scikit-learn (machine learning utilities)
- xgboost (gradient boosting)
- tensorflow (deep learning)
- prophet (time series forecasting)
- statsmodels (statistical models)
- flask (web framework)
- flask-cors (CORS support)
- matplotlib (visualization)
- seaborn (statistical visualization)
- holidays (holiday detection)

**Installation time:** 5-10 minutes depending on internet speed

**Note:** TensorFlow installation may take longer and requires specific system configurations.

---

## Troubleshooting Installation Issues

### Issue 1: TensorFlow Installation Fails

**Problem:** TensorFlow requires specific system configurations

**Solution 1 - Use CPU version:**
```bash
pip install tensorflow-cpu
```

**Solution 2 - Install specific version:**
```bash
pip install tensorflow==2.12.0
```

**Solution 3 - Skip TensorFlow (LSTM won't work):**
Edit `requirements.txt` and comment out the tensorflow line:
```
# tensorflow>=2.12.0
```

### Issue 2: Prophet Installation Fails

**Problem:** Prophet requires additional dependencies

**Windows Solution:**
```bash
pip install pystan==2.19.1.1
pip install prophet
```

**macOS Solution:**
```bash
brew install cmake
pip install prophet
```

**Linux Solution:**
```bash
sudo apt-get install python3-dev
pip install prophet
```

### Issue 3: Permission Denied

**Problem:** Insufficient permissions to install packages

**Solution:**
```bash
pip install --user -r requirements.txt
```

### Issue 4: Package Conflicts

**Problem:** Conflicting package versions

**Solution:** Use a fresh virtual environment:
```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Create new environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

### Issue 5: Slow Installation

**Problem:** Package installation is very slow

**Solution:** Use a faster mirror:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## Verify Installation

### Method 1: Run Quick Test

```bash
python quick_test.py
```

**Expected output:**
```
======================================================================
  QUICK SYSTEM TEST
======================================================================
Testing imports...
✓ All imports successful

Testing data loading...
✓ Loaded 8,944 records for 43 states

Testing preprocessing...
✓ Preprocessed 208 records for California

Testing feature engineering...
✓ Created 20 features

Testing train/test split...
✓ Train: 200 records, Test: 8 records

======================================================================
  TEST RESULTS
======================================================================
Passed: 5/5

✓ All tests passed! System is ready.
```

### Method 2: Check Imports Manually

```bash
python -c "import pandas, numpy, sklearn, xgboost, tensorflow, prophet, statsmodels, flask; print('All packages installed successfully!')"
```

### Method 3: Check Package Versions

```bash
pip list | grep -E "pandas|numpy|sklearn|xgboost|tensorflow|prophet|statsmodels|flask"
```

---

## Post-Installation Setup

### 1. Verify Dataset

```bash
python check_data.py
```

**Expected output:**
- 8,944 total records
- 43 states
- 208 weeks per state
- No missing values

### 2. Run Demo

```bash
python demo.py
```

This will train all models and generate forecasts for California.

### 3. Start API

```bash
python api/app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
```

### 4. Test API

Open a new terminal and run:
```bash
curl http://localhost:5000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "message": "Forecasting API is running"
}
```

---

## Alternative Installation Methods

### Method 1: Using Conda

If you prefer Conda:

```bash
# Create conda environment
conda create -n forecasting python=3.9

# Activate environment
conda activate forecasting

# Install packages
conda install pandas numpy scikit-learn matplotlib seaborn
pip install xgboost tensorflow prophet statsmodels flask flask-cors holidays
```

### Method 2: Using Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "api/app.py"]
```

Build and run:
```bash
docker build -t forecasting-system .
docker run -p 5000:5000 forecasting-system
```

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate environment
deactivate

# Remove directory
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### Remove Packages (if not using virtual environment)

```bash
pip uninstall -r requirements.txt -y
```

---

## System-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Activate virtual environment: `venv\Scripts\activate`
- Some packages may require Visual C++ Build Tools
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### macOS

- May need to install Xcode Command Line Tools: `xcode-select --install`
- Use `python3` instead of `python` if you have Python 2 installed
- Homebrew is recommended for installing dependencies

### Linux

- May need to install development packages:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-dev python3-pip build-essential
  ```
- Use `python3` and `pip3` commands

---

## Getting Help

If you encounter issues:

1. **Check Python version**: `python --version` (must be 3.8+)
2. **Check pip version**: `pip --version`
3. **Try upgrading pip**: `python -m pip install --upgrade pip`
4. **Use virtual environment**: Isolates dependencies
5. **Check error messages**: Often contain solutions
6. **Search online**: Copy error message to Google
7. **Check package documentation**: Each package has installation guides

---

## Next Steps

After successful installation:

1. ✅ Run `python quick_test.py` to verify installation
2. ✅ Run `python check_data.py` to verify dataset
3. ✅ Run `python demo.py` to see the system in action
4. ✅ Read `QUICK_START.md` for usage examples
5. ✅ Read `API_DOCUMENTATION.md` for API details
6. ✅ Start building your forecasts!

---

## Support

For additional help:
- Check `README.md` for general documentation
- Check `QUICK_START.md` for quick start guide
- Check `docs/` folder for detailed documentation
- Review code comments in source files

---

**Installation complete! You're ready to start forecasting! 🚀**
