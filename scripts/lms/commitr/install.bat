@echo off
echo Installing commitr - Git Commit Assistant with LMStudio Integration
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python detected. Installing dependencies...

REM Install the package in development mode
pip install -e .

if errorlevel 1 (
    echo.
    echo Error: Installation failed
    echo Make sure you have pip installed and try again
    pause
    exit /b 1
)

echo.
echo ✅ Installation successful!
echo.
echo You can now use 'commitr' from any directory in your terminal.
echo.
echo Usage examples:
echo   commitr --model gemma-3-4b-it-qat
echo   commitr --model your-model-name --dry-run
echo   commitr --model your-model-name --verbose
echo.
echo Make sure LMStudio is running with your desired model loaded.
echo.
pause
