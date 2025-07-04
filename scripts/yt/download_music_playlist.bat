@echo off
setlocal enabledelayedexpansion

:: Ask for playlist URL
set /p URL=Enter the YouTube playlist URL: 

:: Ask for output folder
set /p OUTDIR=Enter the full path to the output folder: 

:: Run yt-dlp with specified options
yt-dlp -x --audio-format mp3 --embed-thumbnail --embed-metadata ^
-o "%OUTDIR%\%%(uploader)s - %%(title)s.%%(ext)s" ^
"!URL!"

echo.
echo Download complete. Press any key to exit.
pause >nul
