# Shutdown Timeout Script
# Schedules a PC shutdown after specified minutes or cancels scheduled shutdown
# Usage:
#   .\shutdown_timeout.ps1       - Interactive prompt (default: 30 minutes)
#   .\shutdown_timeout.ps1 45    - Shutdown in 45 minutes
#   .\shutdown_timeout.ps1 0     - Cancel scheduled shutdown

if ($args.Count -gt 0) {
    $timeoutMinutes = [int]$args[0]
} else {
    $timeoutMinutes = Read-Host "Enter shutdown timeout in minutes (default: 30, 0 or negative to cancel)"
    
    if ([string]::IsNullOrWhiteSpace($timeoutMinutes)) {
        $timeoutMinutes = 30
    }
    
    $timeoutMinutes = [int]$timeoutMinutes
}

if ($timeoutMinutes -le 0) {
    Write-Host "Cancelling scheduled shutdown..."
    shutdown /a
    exit
}

$timeoutSeconds = $timeoutMinutes * 60

Write-Host "PC will shutdown in $timeoutMinutes minutes ($timeoutSeconds seconds)"
shutdown /s /t $timeoutSeconds