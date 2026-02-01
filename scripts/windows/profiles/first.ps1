# Get the active local IP address used for internet access
$activeIP = Get-NetRoute -DestinationPrefix 0.0.0.0/0 | 
            Get-NetIPAddress -AddressFamily IPv4 | 
            Select-Object -ExpandProperty IPAddress -First 1

# Get the current Wi-Fi SSID
$ssid = (netsh wlan show interfaces | Select-String '^\s+SSID' | ForEach-Object { $_.ToString().Split(':')[1].Trim() })

# Display the info in the terminal
if ($activeIP) {
    Write-Host "Local IP: " -NoNewline
    Write-Host $activeIP -ForegroundColor Cyan -NoNewline
    
    if ($ssid) {
        Write-Host " (SSID: " -NoNewline
        Write-Host $ssid -ForegroundColor Yellow -NoNewline
        Write-Host ")"
    } else {
        Write-Host "" # Just a newline if no SSID found
    }
}
# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}

# Aliases
Set-Alias ytd yt-dlp

# Functions
function updates {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "`n[winget]" -ForegroundColor Cyan
        winget upgrade
    } else {
        Write-Host "`n[winget] not installed" -ForegroundColor Yellow
    }

    if (Get-Command choco -ErrorAction SilentlyContinue) {
        Write-Host "`n[choco]" -ForegroundColor Cyan
        choco outdated
    } else {
        Write-Host "`n[choco] not installed" -ForegroundColor Yellow
    }

    if (Get-Command scoop -ErrorAction SilentlyContinue) {
        Write-Host "`n[scoop]" -ForegroundColor Cyan
        scoop status
    } else {
        Write-Host "`n[scoop] not installed" -ForegroundColor Yellow
    }
}

function upgrade {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "`n[winget]" -ForegroundColor Cyan
        winget upgrade --all --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "`n[winget] not installed" -ForegroundColor Yellow
    }

    if (Get-Command choco -ErrorAction SilentlyContinue) {
        Write-Host "`n[choco]" -ForegroundColor Cyan
        choco upgrade -y all
    } else {
        Write-Host "`n[choco] not installed" -ForegroundColor Yellow
    }

    if (Get-Command scoop -ErrorAction SilentlyContinue) {
        Write-Host "`n[scoop]" -ForegroundColor Cyan
        scoop update *
    } else {
        Write-Host "`n[scoop] not installed" -ForegroundColor Yellow
    }
}

function ytdp {
    param(
        [Parameter(Mandatory=$true, Position=0)]
        [string]$url,
        
        [Parameter(Position=1)]
        [int]$h = 720
    )

    yt-dlp -f "bestvideo[height<=$h]+bestaudio/best[height<=$h]/best" `
           --merge-output-format mp4 `
           --add-metadata `
           --embed-thumbnail `
           --convert-thumbnails jpg `
           -o "%(uploader)s [%(playlist|Single)s] - %(title)s ([%(upload_date)s]).%(ext)s" `
           --no-mtime `
           $url
}

