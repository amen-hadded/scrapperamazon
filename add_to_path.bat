@echo off
REM Add Python Scripts to PATH
REM This script adds C:\Users\hadde\AppData\Roaming\Python\Python312\Scripts to your user PATH

setlocal enabledelayedexpansion

set SCRIPTS_PATH=C:\Users\hadde\AppData\Roaming\Python\Python312\Scripts

echo.
echo Adding %SCRIPTS_PATH% to PATH...
echo.

REM Get current PATH
for /f "tokens=2*" %%A in ('reg query HKCU\Environment /v PATH 2^>nul') do set CURRENT_PATH=%%B

REM Check if path already exists
echo !CURRENT_PATH! | find /I "%SCRIPTS_PATH%" >nul
if errorlevel 1 (
    REM Path not found, add it
    reg add HKCU\Environment /v PATH /t REG_EXPAND_SZ /d "!CURRENT_PATH!;%SCRIPTS_PATH%" /f >nul 2>&1
    if errorlevel 0 (
        echo ✓ Successfully added to PATH!
        echo.
        echo IMPORTANT: You need to RESTART your terminal for changes to take effect.
        echo After restarting, you can use: scrapperAmazon scrape -q "laptop"
    ) else (
        echo ✗ Failed to add to PATH
    )
) else (
    echo * Path is already in PATH!
)

pause
