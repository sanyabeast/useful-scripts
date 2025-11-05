@echo off
setlocal enabledelayedexpansion

:: Check if folder was passed via drag-and-drop
if "%~1"=="" (
    set /p TARGET_FOLDER=Enter folder path to process: 
) else (
    set "TARGET_FOLDER=%~1"
)

:: Verify folder exists
if not exist "%TARGET_FOLDER%" (
    echo [!] Folder not found: "%TARGET_FOLDER%"
    goto end
)

:: Prompt for model (default: google/gemma-3-12b)
set /p MODEL=Enter model name [default: google/gemma-3-12b]: 
if "!MODEL!"=="" set MODEL=google/gemma-3-12b

:: Prompt for recursive mode
set /p RECURSE=Run recursively? (y/n): 
set "RECURSIVE_FLAG="
if /i "!RECURSE!"=="y" set "RECURSIVE_FLAG=--recursive"

:: Prompt for threshold value
set /p THRESHOLD=Enter threshold value (0.0-1.0) [default: 0.4]: 
if "!THRESHOLD!"=="" set THRESHOLD=0.4

:: Prompt for force mode
set /p FORCE=Force rename all files regardless of quality? (y/n) [default: n]: 
set "FORCE_FLAG="
if /i "!FORCE!"=="y" set "FORCE_FLAG=--force"

:: Show confirmation with parameter preview
echo.
echo ----------------------------------------
echo PARAMETER SUMMARY:
echo ----------------------------------------
echo Target folder: "!TARGET_FOLDER!"
echo Model: !MODEL!
echo Recursive: !RECURSE!
if "!RECURSIVE_FLAG!"=="--recursive" (
    echo [x] Will process all subfolders
) else (
    echo [ ] Only processing top-level folder
)
echo Threshold: !THRESHOLD!
if "!FORCE_FLAG!"=="--force" (
    echo [x] Force renaming all files
) else (
    echo [ ] Only renaming files with quality score below !THRESHOLD!
)
echo ----------------------------------------
echo.

:: Ask for confirmation
set /p CONFIRM=Proceed with these settings? (y/n): 
if /i not "!CONFIRM!"=="y" (
    echo Operation cancelled by user.
    goto end
)

:: Run the Python script
echo.
echo Running:
echo python "D:\osProjects\useful-scripts\scripts\lms\image_namer\main.py" --model !MODEL! --folder "!TARGET_FOLDER!" !RECURSIVE_FLAG! --threshold !THRESHOLD! !FORCE_FLAG!
echo.

:: Use call to ensure batch file continues after Python script completes
call python "D:\osProjects\useful-scripts\scripts\lms\image_namer\main.py" --model !MODEL! --folder "!TARGET_FOLDER!" !RECURSIVE_FLAG! --threshold !THRESHOLD! !FORCE_FLAG!
if errorlevel 1 (
    echo.
    echo [!] Python script exited with an error.
)

:end
echo.
echo ----------------------------------------
echo Done. Press any key to exit...
pause >nul
