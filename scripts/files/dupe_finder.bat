@echo off
setlocal enabledelayedexpansion

echo === Duplicate File Finder ===
echo.

REM Get the directory where the batch file is located
set "script_dir=%~dp0"

REM Check if a folder was dropped onto the batch file
set "input_dir=%~1"
if not "%input_dir%"=="" (
    echo Detected dropped folder: %input_dir%
    echo.
    
    REM Run the Python script with the full path to ensure it's found
    python "%script_dir%dupe_finder.py" "%input_dir%"
    
    REM Keep the window open after execution
    echo.
    echo Press any key to exit...
    pause > nul
) else (
    REM Run in fully interactive mode
    python "%script_dir%dupe_finder.py" --interactive
)
