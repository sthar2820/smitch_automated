@echo off
chcp 65001 > nul
title SMITCH Production Auto-Watcher
color 0B
echo.
echo ================================================
echo    SMITCH PRODUCTION AUTO-WATCHER
echo ================================================
echo.
echo Production-grade file monitoring with:
echo   - Health monitoring and statistics
echo   - Error handling and notifications  
echo   - Automatic recovery and logging
echo   - Performance optimization
echo.
echo Source: C:\Users\sthar\Downloads\SMITCH_2025\SMITCH_2025
echo Output: C:\Users\sthar\Downloads\smitch_extracted
echo Logs: ./logs/
echo.
echo Press any key to start production monitoring...
pause > nul
echo.
echo Starting production watcher...
python production_watcher.py
echo.
echo Production watcher has stopped.
echo Check logs/ folder for detailed information.
pause
