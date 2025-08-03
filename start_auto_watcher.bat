@echo off
chcp 65001 > nul
title SMITCH Production Auto-Watcher
color 0B

:MAIN_MENU
cls
echo.
echo ================================================
echo    SMITCH PRODUCTION AUTO-WATCHER v2.0
echo ================================================
echo.
echo Production-grade file monitoring with:
echo   - Health monitoring and statistics
echo   - Error handling and notifications  
echo   - Automatic recovery and logging
echo   - Performance optimization
echo   - Auto-restart capability
echo.
echo Source: C:\Users\RShrestha\OneDrive - Dura-Shiloh\SMITCH_2025
echo Output: C:\Users\RShrestha\OneDrive - Dura-Shiloh\smitch_extracted
echo Logs: ./logs/
echo.
echo [1] Start Watcher (Run Once)
echo [2] Start Watcher (Persistent - Auto Restart)
echo [3] Test Configuration
echo [4] Process Existing Files
echo [5] Exit
echo.
set /p choice="Choose an option (1-5): "

if "%choice%"=="1" goto RUN_ONCE
if "%choice%"=="2" goto RUN_PERSISTENT
if "%choice%"=="3" goto TEST_CONFIG
if "%choice%"=="4" goto PROCESS_FILES
if "%choice%"=="5" goto EXIT
goto MAIN_MENU

:RUN_ONCE
echo.
echo Starting production watcher (single run)...
"C:/Users/RShrestha/AppData/Local/Programs/Python/Python313/python.exe" production_watcher.py
echo.
echo Production watcher has stopped.
echo Check logs/ folder for detailed information.
pause
goto MAIN_MENU

:RUN_PERSISTENT
echo.
echo Starting production watcher in PERSISTENT mode...
echo Press Ctrl+C to stop completely
echo.
:RESTART_LOOP
echo [%date% %time%] Starting watcher...
"C:/Users/RShrestha/AppData/Local/Programs/Python/Python313/python.exe" production_watcher.py
echo.
echo [%date% %time%] Watcher stopped. Restarting in 5 seconds...
echo Press Ctrl+C now to exit, or wait for restart...
timeout /t 5 /nobreak >nul
goto RESTART_LOOP

:TEST_CONFIG
echo.
echo Testing configuration...
"C:/Users/RShrestha/AppData/Local/Programs/Python/Python313/python.exe" -c "from config import Config; result = Config.validate(); print('Configuration Valid:', result['valid']); print('Issues:', result['issues']) if result['issues'] else print('No issues found'); print('Warnings:', result['warnings']) if result['warnings'] else print('No warnings')"
echo.
pause
goto MAIN_MENU

:PROCESS_FILES
echo.
echo Processing existing files...
"C:/Users/RShrestha/AppData/Local/Programs/Python/Python313/python.exe" test_runner.py
echo.
pause
goto MAIN_MENU

:EXIT
echo.
echo Goodbye!
timeout /t 2 >nul
exit
