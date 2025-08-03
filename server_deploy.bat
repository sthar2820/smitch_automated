@echo off
title SMITCH Server Deployment Tool
color 0C
echo.
echo ================================================
echo    SMITCH COMPANY SERVER DEPLOYMENT
echo ================================================
echo.
echo This script will prepare SMITCH Auto-Watcher for
echo production deployment on a Windows Server.
echo.
echo Requirements:
echo   - Windows Server 2016+ or Windows 10+
echo   - Python 3.8+ (will be installed if missing)
echo   - Administrator privileges
echo   - Network access to SharePoint
echo.

:ADMIN_CHECK
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges.
    echo Please run as Administrator.
    pause
    exit /b 1
)

:MENU
echo ============ DEPLOYMENT OPTIONS ============
echo.
echo 1. Install Python and Dependencies
echo 2. Configure SharePoint Paths
echo 3. Install as Windows Service
echo 4. Test Configuration
echo 5. Start Production Service
echo 6. View Service Status
echo 7. Uninstall Service
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto INSTALL_PYTHON
if "%choice%"=="2" goto CONFIGURE_PATHS
if "%choice%"=="3" goto INSTALL_SERVICE
if "%choice%"=="4" goto TEST_CONFIG
if "%choice%"=="5" goto START_SERVICE
if "%choice%"=="6" goto SERVICE_STATUS
if "%choice%"=="7" goto UNINSTALL_SERVICE
if "%choice%"=="8" goto EXIT

:INSTALL_PYTHON
echo.
echo ============ INSTALLING PYTHON ============
echo.
echo Checking Python installation...
python --version >nul 2>&1
if %errorLevel% equ 0 (
    echo Python is already installed.
    python --version
) else (
    echo Python not found. Please install Python 3.8+ manually.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    goto MENU
)

echo.
echo Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt
pip install pywin32

echo.
echo Python and dependencies installed successfully!
pause
goto MENU

:CONFIGURE_PATHS
echo.
echo ============ SHAREPOINT CONFIGURATION ============
echo.
echo Configure paths for your SharePoint environment:
echo.
echo Example SharePoint paths:
echo   Input:  \\server\SharePoint\SMITCH_2025
echo   Output: \\server\SharePoint\SMITCH_Extracted
echo.
echo Or OneDrive Business paths:
echo   Input:  C:\SharePoint\Company\SMITCH_2025
echo   Output: C:\SharePoint\Company\SMITCH_Extracted
echo.
set /p input_path="Enter SMITCH input path: "
set /p output_path="Enter extracted output path: "

echo.
echo Creating server configuration...
(
echo # SMITCH Server Configuration - %date% %time%
echo # Configured for: %COMPUTERNAME%
echo.
echo # SharePoint Paths
echo WATCH_PATH=%input_path%
echo OUTPUT_PATH=%output_path%
echo.
echo # Server Settings
echo SHAREPOINT_MODE=true
echo NETWORK_TIMEOUT=60
echo RETRY_ATTEMPTS=5
echo.
echo # Logging
echo LOG_PATH=C:\SMITCH_Logs
echo LOG_LEVEL=INFO
echo.
echo # Processing Settings
echo COOLDOWN_SECONDS=15
echo TIMEOUT_SECONDS=300
echo MAX_FILE_SIZE_MB=200
echo.
echo # Health Monitoring
echo HEALTH_CHECK_INTERVAL=600
echo.
echo # Email Notifications (Optional)
echo # SMTP_SERVER=smtp.company.com
echo # SMTP_PORT=587
echo # EMAIL_USER=smitch-alerts@company.com
echo # EMAIL_PASSWORD=your-password
echo # NOTIFICATION_EMAILS=admin@company.com,team@company.com
) > .env

echo.
echo Creating log directory...
mkdir "C:\SMITCH_Logs" 2>nul

echo.
echo Server configuration completed!
echo Configuration saved to .env file.
pause
goto MENU

:INSTALL_SERVICE
echo.
echo ============ INSTALLING WINDOWS SERVICE ============
echo.
echo Installing SMITCH Auto-Watcher as Windows Service...
python windows_service.py install

if %errorLevel% equ 0 (
    echo.
    echo Service installed successfully!
    echo.
    echo Service Details:
    echo   Name: SMITCHWatcher
    echo   Display Name: SMITCH File Watcher Service
    echo   Startup Type: Automatic
    echo   Log On As: Local System
    echo.
    echo The service will start automatically when the server boots.
) else (
    echo.
    echo Service installation failed!
    echo Please check that you're running as Administrator.
)
pause
goto MENU

:TEST_CONFIG
echo.
echo ============ TESTING CONFIGURATION ============
echo.
echo Testing SMITCH configuration...
python -c "
from config import Config
import os

print('Configuration Test Results:')
print('=' * 40)

# Test configuration
result = Config.validate()
if result['valid']:
    print('✓ Configuration is VALID')
else:
    print('✗ Configuration has issues:')
    for issue in result['issues']:
        print(f'  - {issue}')

if result.get('warnings'):
    print('\nWarnings:')
    for warning in result['warnings']:
        print(f'  ! {warning}')

print(f'\nPaths:')
print(f'  Input:  {Config.WATCH_PATH}')
print(f'  Output: {Config.OUTPUT_PATH}')
print(f'  Logs:   {Config.LOG_PATH}')

print(f'\nSettings:')
print(f'  SharePoint Mode: {Config.SHAREPOINT_MODE}')
print(f'  Cooldown: {Config.COOLDOWN_SECONDS}s')
print(f'  Timeout: {Config.TIMEOUT_SECONDS}s')

# Test file access
print(f'\nFile Access Test:')
print(f'  Input folder exists: {os.path.exists(Config.WATCH_PATH)}')
print(f'  Output folder exists: {os.path.exists(Config.OUTPUT_PATH)}')
print(f'  Log folder exists: {os.path.exists(Config.LOG_PATH)}')
"

echo.
echo Configuration test completed!
pause
goto MENU

:START_SERVICE
echo.
echo ============ STARTING SERVICE ============
echo.
echo Starting SMITCH Auto-Watcher Service...
net start SMITCHWatcher

if %errorLevel% equ 0 (
    echo.
    echo Service started successfully!
    echo SMITCH Auto-Watcher is now monitoring files.
    echo.
    echo Monitor service activity:
    echo   - Windows Event Viewer ^> Windows Logs ^> Application
    echo   - Log files in C:\SMITCH_Logs\
) else (
    echo.
    echo Failed to start service!
    echo Check Windows Event Viewer for error details.
)
pause
goto MENU

:SERVICE_STATUS
echo.
echo ============ SERVICE STATUS ============
echo.
sc query SMITCHWatcher
echo.
echo Recent log entries:
if exist "C:\SMITCH_Logs\auto_watcher.log" (
    echo.
    echo Last 10 lines from auto_watcher.log:
    powershell "Get-Content 'C:\SMITCH_Logs\auto_watcher.log' -Tail 10"
) else (
    echo No log file found yet.
)
echo.
pause
goto MENU

:UNINSTALL_SERVICE
echo.
echo ============ UNINSTALLING SERVICE ============
echo.
echo Stopping service...
net stop SMITCHWatcher 2>nul

echo Removing service...
python windows_service.py remove

echo.
echo Service uninstalled.
pause
goto MENU

:EXIT
echo.
echo ============ DEPLOYMENT SUMMARY ============
echo.
echo SMITCH Auto-Watcher Server Deployment Complete!
echo.
echo Next Steps:
echo   1. Verify service is running
echo   2. Test with a sample Excel file
echo   3. Monitor logs for any issues
echo   4. Train team members on usage
echo.
echo Support Files:
echo   - documentation\ (Complete documentation)
echo   - documentation\TEAM_HANDOVER.md (Team guide)
echo   - documentation\SHAREPOINT_SETUP.md (SharePoint guide)
echo   - logs\ (Runtime logs and statistics)
echo.
pause
exit
