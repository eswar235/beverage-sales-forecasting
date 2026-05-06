@echo off
REM ========================================
REM  Video Recording Commands
REM  Copy and paste these one by one!
REM ========================================

echo.
echo ========================================
echo   SCENE 1: Check Data
echo ========================================
python check_data.py
pause

echo.
echo ========================================
echo   SCENE 2: Quick Test
echo ========================================
python quick_test.py
pause

echo.
echo ========================================
echo   SCENE 3: Main Demo (This is the big one!)
echo ========================================
python demo.py
pause

echo.
echo ========================================
echo   SCENE 4: Show Visualization
echo ========================================
start models\California_forecast_comparison.png
pause

echo.
echo ========================================
echo   SCENE 5: Train Multiple States
echo ========================================
python train_models.py Texas Florida
pause

echo.
echo ========================================
echo   SCENE 6: Start API
echo ========================================
echo Starting API server...
echo Open a NEW terminal for testing!
python api/app.py
