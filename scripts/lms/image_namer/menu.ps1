param(
    [string]$FolderPath
)

function Show-Banner {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Image Namer - LMStudio Integration" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Get-UserInput {
    param(
        [string]$Prompt,
        [string]$Default = ""
    )
    
    if ($Default) {
        $userInput = Read-Host "$Prompt [default: $Default]"
        if ([string]::IsNullOrWhiteSpace($userInput)) {
            return $Default
        }
        return $userInput
    }
    
    return Read-Host $Prompt
}

function Get-YesNoInput {
    param(
        [string]$Prompt,
        [string]$Default = "n"
    )
    
    $userInput = Read-Host "$Prompt (y/n) [default: $Default]"
    if ([string]::IsNullOrWhiteSpace($userInput)) {
        return $Default
    }
    return $userInput.ToLower()
}

Show-Banner

if ([string]::IsNullOrWhiteSpace($FolderPath)) {
    $targetFolder = Get-UserInput "Enter folder path to process"
} else {
    $targetFolder = $FolderPath
    Write-Host "Using dropped folder: $targetFolder" -ForegroundColor Green
    Write-Host ""
}

if (-not (Test-Path $targetFolder)) {
    Write-Host "[!] Folder not found: $targetFolder" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

$model = Get-UserInput "Enter model name" "google/gemma-3-12b"
$recurse = Get-YesNoInput "Run recursively?"
$threshold = Get-UserInput "Enter threshold value (0.0-1.0)" "0.4"
$force = Get-YesNoInput "Force rename all files regardless of quality?"

$recursiveFlag = if ($recurse -eq "y") { "--recursive" } else { "" }
$forceFlag = if ($force -eq "y") { "--force" } else { "" }

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host "PARAMETER SUMMARY:" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host "Target folder: `"$targetFolder`""
Write-Host "Model: $model"
Write-Host "Recursive: $recurse"
if ($recursiveFlag) {
    Write-Host "[x] Will process all subfolders" -ForegroundColor Green
} else {
    Write-Host "[ ] Only processing top-level folder" -ForegroundColor Gray
}
Write-Host "Threshold: $threshold"
if ($forceFlag) {
    Write-Host "[x] Force renaming all files" -ForegroundColor Green
} else {
    Write-Host "[ ] Only renaming files with quality score below $threshold" -ForegroundColor Gray
}
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""

$confirm = Get-YesNoInput "Proceed with these settings?"
if ($confirm -ne "y") {
    Write-Host "Operation cancelled by user." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

$scriptPath = Join-Path $PSScriptRoot "main.py"
$pythonArgs = @("--model", $model, "--folder", $targetFolder, "--threshold", $threshold)
if ($recursiveFlag) { $pythonArgs += $recursiveFlag }
if ($forceFlag) { $pythonArgs += $forceFlag }

$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $pythonCmd = $cmd
        break
    }
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "[!] Python not found. Please install Python or add it to PATH." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Running:" -ForegroundColor Cyan
Write-Host "$pythonCmd `"$scriptPath`" $($pythonArgs -join ' ')" -ForegroundColor Gray
Write-Host ""

try {
    & $pythonCmd $scriptPath $pythonArgs
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[!] Python script exited with an error." -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "[!] Error running Python script: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "Done. Press any key to exit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
