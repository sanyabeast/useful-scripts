param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("0", "1")]
    [string]$State
)

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script must be run as Administrator. Please run PowerShell as Administrator and try again."
    exit 1
}

if ($State -eq "0") {
    Write-Host "Disabling Bluetooth service..." -ForegroundColor Yellow
    try {
        Stop-Service bthserv -Force
        Set-Service bthserv -StartupType Disabled
        Write-Host "Bluetooth service disabled successfully." -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to disable Bluetooth service: $($_.Exception.Message)"
        exit 1
    }
}
elseif ($State -eq "1") {
    Write-Host "Enabling Bluetooth service..." -ForegroundColor Yellow
    try {
        Set-Service bthserv -StartupType Automatic
        Start-Service bthserv
        Write-Host "Bluetooth service enabled successfully." -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to enable Bluetooth service: $($_.Exception.Message)"
        exit 1
    }
}
