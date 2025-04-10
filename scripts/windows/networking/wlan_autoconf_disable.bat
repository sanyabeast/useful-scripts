@echo off
:: Specify the Wi-Fi interface name here
set INTERFACE_NAME=Wi-Fi

:: Check for administrative permissions
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit
)

:: The command that requires administrative privileges
:: netsh wlan set autoconfig enabled=no interface="%INTERFACE_NAME%":
:: Uses the specified interface name to disable the autoconfig setting.

netsh wlan set autoconfig enabled=no interface="%INTERFACE_NAME%"

pause