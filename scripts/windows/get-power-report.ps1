# get-power-report.ps1 (safe, wide date range, no emoji)

$ErrorActionPreference = 'SilentlyContinue'
chcp 65001 > $null

Write-Host ""
Write-Host "=== System Power Event Report (Last 30 Days) ===" -ForegroundColor Cyan
Write-Host ""

$events = Get-WinEvent -LogName System |
    Where-Object {
        ($_.Id -in 41, 42, 1074, 6005, 6006, 6008) -and
        ($_.TimeCreated -gt (Get-Date).AddDays(-30))
    } |
    Sort-Object TimeCreated -Descending

if (-not $events) {
    Write-Host "No recent power-related events found." -ForegroundColor Yellow
    pause
    exit
}

foreach ($event in $events) {
    $time = $event.TimeCreated.ToString("dd.MM.yyyy HH:mm:ss")
    $id = $event.Id
    $msg = $event.Message.Trim()

    switch ($id) {
        41 {
            Write-Host "[CRITICAL] [$time] System rebooted without clean shutdown (ID 41)" -ForegroundColor Red
        }
        6008 {
            Write-Host "[ERROR   ] [$time] Unexpected shutdown detected (ID 6008)" -ForegroundColor DarkYellow
        }
        6006 {
            Write-Host "[INFO    ] [$time] Event Log stopped (shutdown) (ID 6006)" -ForegroundColor Gray
        }
        6005 {
            Write-Host "[INFO    ] [$time] Event Log started (boot) (ID 6005)" -ForegroundColor Green
        }
        1074 {
            if ($msg -match "shutdown") {
                Write-Host "[USER    ] [$time] Shutdown requested (ID 1074)" -ForegroundColor Blue
            } elseif ($msg -match "restart") {
                Write-Host "[USER    ] [$time] Restart requested (ID 1074)" -ForegroundColor Blue
            } else {
                Write-Host "[USER    ] [$time] Power event (ID 1074)" -ForegroundColor Blue
            }
        }
        42 {
            Write-Host "[SLEEP   ] [$time] System entered sleep mode (ID 42)" -ForegroundColor Magenta
        }
    }
}

Write-Host ""
Write-Host "=== End of Report ===" -ForegroundColor Cyan
Write-Host ""
pause
