<#
.SYNOPSIS
    Restores Microsoft Defender's preferences to their default, more secure configuration.

.DESCRIPTION
    This script reverts the changes made by the 'defender_relax.ps1' script. It sets key
    Microsoft Defender preferences back to their standard values, including:

    - Resetting the average CPU load factor for scans to its default (50%).
    - Enabling scanning of network files.
    - Enabling archive scanning by removing the specific registry key entry.
    - Enabling email scanning.
    - Re-enabling cloud-delivered protection and automatic sample submission.

.NOTES
    - This script must be run with Administrator privileges.
    - It modifies the system registry, but only to remove a specific, known key.
    - The restored settings may result in increased CPU usage during scans and slightly longer scan times,
      as Defender will be performing a more thorough analysis.

.EXAMPLE
    .\defender_restore.ps1
    Runs the script to restore all Microsoft Defender settings to their default state.
#>

# Check for Administrator privileges
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script must be run with Administrator privileges. Please re-run as an Administrator." -ForegroundColor Red
    Start-Sleep -Seconds 5
    Exit
}

Write-Host "Restoring Microsoft Defender to a secure state..." -ForegroundColor Yellow

try {
    # Restore core preferences using the PowerShell command
    Write-Host "Restoring ScanAvgCPULoadFactor to default (50%)..." -ForegroundColor Green
    Set-MpPreference -ScanAvgCPULoadFactor 50 -ErrorAction Stop

    Write-Host "Enabling network file scanning..." -ForegroundColor Green
    Set-MpPreference -DisableScanningNetworkFiles $false -ErrorAction Stop

    Write-Host "Enabling email scanning..." -ForegroundColor Green
    Set-MpPreference -DisableEmailScanning $false -ErrorAction Stop

    Write-Host "Enabling automatic sample submission and cloud protection..." -ForegroundColor Green
    Set-MpPreference -MAPSReporting 2 -ErrorAction Stop
    Set-MpPreference -SubmitSamplesConsent 1 -ErrorAction Stop
    Set-MpPreference -CloudBlockLevel "High" -ErrorAction Stop

    # Remove the registry key to re-enable archive scanning
    Write-Host "Removing registry key for archive scanning..." -ForegroundColor Yellow
    $registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Scan"
    $valueName = "DisableArchiveScanning"

    if (Test-Path -Path $registryPath) {
        Remove-ItemProperty -Path $registryPath -Name $valueName -ErrorAction SilentlyContinue
        Write-Host "Registry key for archive scanning has been removed." -ForegroundColor Green
    } else {
        Write-Host "Registry path '$registryPath' does not exist. No action needed." -ForegroundColor Yellow
    }
    
    Write-Host "All settings have been restored successfully." -ForegroundColor Green
    
} catch {
    Write-Host "An error occurred while trying to restore Defender preferences." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "You can verify the changes by running: Get-MpPreference" -ForegroundColor Cyan
