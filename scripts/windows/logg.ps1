<#
.SYNOPSIS
    Logs a given string to a log file with a date and time stamp.

.DESCRIPTION
    This script takes a single string parameter and appends it to a log file
    in the same directory as the script itself. The log file name is
    automatically derived from the script's name. Each entry is prepended
    with the current date and time.

.PARAMETER LogMessage
    The string message to be written to the log file.

.NOTES
    The script will automatically create the log file if it does not exist.
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory=$true, Position=0)]
    [string]$LogMessage
)

# Define the log file name and path dynamically
$ScriptBaseName = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Name)
$LogFileName = "$ScriptBaseName.log"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFilePath = Join-Path -Path $ScriptDir -ChildPath $LogFileName

# Get the current date and time in a readable format
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Format the log entry
$LogEntry = "$timestamp - $LogMessage"

# Append the new line to the log file
Add-Content -Path $LogFilePath -Value $LogEntry

# Output a confirmation message to the console
Write-Host "Log entry added to '$LogFilePath'."
