 # Network Adapter Toggle Script
# 
# Purpose: Enable or disable all network adapters on the system
# Usage:   .\toggle_net_adapter.ps1 [0|1]
#          0 = Disable all network adapters
#          1 = Enable all network adapters
#
# Author:  Created for useful-scripts collection
# Date:    September 2025
# 
# Note: This script affects ALL network adapters (Wi-Fi, Ethernet, etc.)
#       Requires Administrator privileges to modify network adapters

param(
    [Parameter(Mandatory=$true, HelpMessage="Enter 0 to disable or 1 to enable all network adapters")]
    [ValidateSet("0", "1")]
    [string]$Action
)

# Enable all network adapters
if ($Action -eq "1") {
    Write-Host "Enabling all network adapters..." -ForegroundColor Green
    Get-NetAdapter | Enable-NetAdapter -Confirm:$false
    Write-Host "All network adapters enabled successfully" -ForegroundColor Green
} 
# Disable all network adapters
elseif ($Action -eq "0") {
    Write-Host "Disabling all network adapters..." -ForegroundColor Yellow
    Get-NetAdapter | Disable-NetAdapter -Confirm:$false
    Write-Host "All network adapters disabled successfully" -ForegroundColor Yellow
}