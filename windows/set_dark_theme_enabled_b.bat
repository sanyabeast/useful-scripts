@echo off
setlocal enabledelayedexpansion

REM Check for command line argument
if "%~1"=="" (
    echo Usage: %0 [on|off]
    exit /b
)

REM Set the Registry key for Apps based on the argument
if /i "%~1"=="on" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v "AppsUseLightTheme" /t REG_DWORD /d 0 /f
    echo Dark theme for apps turned ON.
) else if /i "%~1"=="off" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v "AppsUseLightTheme" /t REG_DWORD /d 1 /f
    echo Dark theme for apps turned OFF.
) else (
    echo Invalid argument. Use "on" or "off".
)

endlocal