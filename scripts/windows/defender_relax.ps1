<#
.SYNOPSIS
    Configures Microsoft Defender to a "relaxed" state by minimizing its CPU usage and disabling
    several non-essential scanning features.

.DESCRIPTION
    This script is the third version designed to address a persistent issue with the
    'DisableArchiveScanning' setting. It sets several key preferences for Microsoft Defender
    and directly modifies the registry to ensure the archive scanning setting is disabled.

    It includes:
    - Setting the average CPU load factor for scans to the minimum (5%).
    - Disabling scanning of network files.
    - Disabling scanning of archive files by directly manipulating the registry.
    - Disabling email scanning.
    - Disabling cloud-delivered protection and automatic sample submission.

.NOTES
    - This script must be run with Administrator privileges.
    - Directly editing the registry can be risky if done incorrectly. This script targets a
      specific known key for Microsoft Defender settings.
    - These changes may increase scan times and slightly reduce overall protection effectiveness.

.EXAMPLE
    .\Set-DefenderPreferences_v3.ps1
    Runs the script to apply all of the relaxed settings, including the registry modification.
#>

# Check for Administrator privileges
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script must be run with Administrator privileges. Please re-run as an Administrator." -ForegroundColor Red
    Start-Sleep -Seconds 5
    Exit
}

Write-Host "Configuring Microsoft Defender to a relaxed state..." -ForegroundColor Yellow

try {
    # Set core preferences using the PowerShell command
    Write-Host "Setting ScanAvgCPULoadFactor to 5%..." -ForegroundColor Green
    Set-MpPreference -ScanAvgCPULoadFactor 5 -ErrorAction Stop

    Write-Host "Disabling network file scanning..." -ForegroundColor Green
    Set-MpPreference -DisableScanningNetworkFiles $true -ErrorAction Stop

    Write-Host "Disabling email scanning..." -ForegroundColor Green
    Set-MpPreference -DisableEmailScanning $true -ErrorAction Stop

    Write-Host "Disabling automatic sample submission..." -ForegroundColor Green
    Set-MpPreference -MAPSReporting 0 -ErrorAction Stop
    Set-MpPreference -SubmitSamplesConsent 0 -ErrorAction Stop
    Set-MpPreference -CloudBlockLevel 0 -ErrorAction Stop

    # Directly modify the registry to disable archive scanning, as Set-MpPreference can be unreliable for this setting
    Write-Host "Disabling archive scanning via registry key..." -ForegroundColor Yellow
    $registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Scan"
    $valueName = "DisableArchiveScanning"
    $valueData = 1

    if (-not (Test-Path $registryPath)) {
        Write-Host "Creating registry path: $registryPath" -ForegroundColor Cyan
        New-Item -Path $registryPath -Force | Out-Null
    }

    Set-ItemProperty -Path $registryPath -Name $valueName -Value $valueData -Type DWORD -Force -ErrorAction Stop
    Write-Host "Registry key for archive scanning has been updated." -ForegroundColor Green
    
    Write-Host "All settings have been applied successfully." -ForegroundColor Green
    
} catch {
    Write-Host "An error occurred while trying to set Defender preferences." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "You can verify the changes by running: Get-MpPreference" -ForegroundColor Cyan
