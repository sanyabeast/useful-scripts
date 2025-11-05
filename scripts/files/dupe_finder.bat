@echo off
setlocal enabledelayedexpansion

echo === Duplicate File Finder ===
echo.

set "script_dir=%~dp0"

set "input_dir1=%~1"
set "input_dir2=%~2"

if not "%input_dir1%"=="" (
    if not "%input_dir2%"=="" (
        echo Detected two folders for cross-folder comparison:
        echo Folder 1: %input_dir1%
        echo Folder 2: %input_dir2%
        echo.
        
        python "%script_dir%dupe_finder.py" "%input_dir1%" "%input_dir2%"
    ) else (
        echo Detected single folder: %input_dir1%
        echo.
        
        python "%script_dir%dupe_finder.py" "%input_dir1%"
    )
    
    echo.
    echo Press any key to exit...
    pause > nul
) else (
    python "%script_dir%dupe_finder.py" --interactive
)
