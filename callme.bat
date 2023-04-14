@echo off

REM Get the script name and directory
set "SCRIPT_NAME=%~nx0"
set "SCRIPT_DIR=%~dp0"

REM Create the log file name
set "LOG_FILE=%SCRIPT_DIR%%~n0.log"

REM Get the current date and time
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set "DATETIME=%date% %%a:%%b:%%c"
)

REM Get the command line arguments
set "ARGS=%*"

REM Get the name of the function or script that called this function
if "%~0"=="%SCRIPT_NAME%" (
    set "CALLER=%SCRIPT_NAME%"
) else (
    set "CALLER=%~0"
)

REM Log the message
echo %DATETIME%: %ARGS% >> "%LOG_FILE%"