@echo off
setlocal enabledelayedexpansion

set "folder=%~1"
if not defined folder set "folder=%cd%"

set "count=0"
for /r "%folder%" %%f in (*.jfif) do (
  ren "%%f" "%%~nf.jpg"
  set /a "count+=1"
)

echo Renamed %count% files.