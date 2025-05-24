@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo Image Dataset Maker - Interactive Mode
echo ========================================================
echo.

REM Check if a folder was dropped onto the batch file
set "drag_drop_folder=%~1"

REM Ask for required parameters
if not "!drag_drop_folder!"=="" (
    echo Detected drag-and-drop folder: !drag_drop_folder!
    set "input_folder=!drag_drop_folder!"
    echo.
) else (
    set /p input_folder=Enter input folder path: 
)

set /p output_folder=Enter output folder path: 

REM Check if required parameters are provided
if "!input_folder!"=="" (
    echo Error: Input folder is required.
    goto :end
)

if "!output_folder!"=="" (
    echo Error: Output folder is required.
    goto :end
)

REM Ask for optional parameters with defaults
set /p model=Enter model name (default: gemma-3-4b-it-qat): 
if "!model!"=="" set model=gemma-3-4b-it-qat

set /p start_index=Enter starting index (default: 1): 
if "!start_index!"=="" set start_index=1

set /p padding=Enter padding (number of digits, default: 4): 
if "!padding!"=="" set padding=4

set /p recursive=Include subfolders? (y/n, default: n): 
set recursive_flag=
if /i "!recursive!"=="y" set recursive_flag=-r

set /p prefix=Enter prefix for descriptions (optional): 
set prefix_flag=
if not "!prefix!"=="" set prefix_flag=--prefix "!prefix!"

set /p prompt=Enter prompt context for LLM (optional): 
set prompt_flag=
if not "!prompt!"=="" set prompt_flag=--prompt "!prompt!"

set /p resolutions=Enter resolutions (space-separated, default: "512 768 1024"): 
set resolution_flag=
if "!resolutions!"=="" (
    set resolution_flag=--resolution "512 768 1024"
) else (
    set resolution_flag=--resolution "!resolutions!"
)

echo.
echo ========================================================
echo Running with the following parameters:
echo ========================================================
echo Input folder: !input_folder!
echo Output folder: !output_folder!
echo Model: !model!
echo Start index: !start_index!
echo Padding: !padding!
echo Include subfolders: !recursive!
if not "!prefix!"=="" echo Prefix: !prefix!
if not "!prompt!"=="" echo Prompt context: !prompt!
if "!resolutions!"=="" (
    echo Resolutions: 512 768 1024
) else (
    echo Resolutions: !resolutions!
)
echo ========================================================
echo.

REM Confirm before running
set /p confirm=Continue? (y/n): 
if /i not "!confirm!"=="y" goto :end

echo.
echo Running script...
echo.

REM Run the script with all parameters
python main.py -i "!input_folder!" -o "!output_folder!" -m "!model!" --start-index !start_index! --padding !padding! !recursive_flag! !prefix_flag! !prompt_flag! !resolution_flag!

:end
echo.
pause
