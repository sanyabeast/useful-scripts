:setup
@echo off
echo PRESS ENTER EVERYWHERE TO SKIP AND USE DEFAULTS
echo . . . 

cd %1

echo SOURCE OF FRAMES: %1

set PATTERN=0%%3d.png
echo ENTER FRAME FILES PATTERN (DEFAULT: 0%%3d.png)
set /P PATTERN=""

set FPS=30
echo ENTER TARGET FPS (DEFAULT: 30)
set /P FPS=""

set MINRATE=5000
echo ENTER MINIMUM BITRATE (DEFAULT: 5000)
set /P MINRATE=""

set MAXRATE=5000
echo ENTER MAXIMUM BITRATE (DEFAULT: 5000)
set /P MAXRATE=""

set OUTPUT=output.webm
echo ENTER OUTPUT FILE NAME (DEFAULT: output.webm)
set /P OUTPUT=""

echo . . . 
echo SUMMARY:
echo SOURCE: %1
echo PATTERN "%PATTERN%"
echo TARGET FPS: %FPS%
echo MIN BITRATE: %MINRATE%
echo MAX BITRATE: %MAXRATE%
echo OUTPUT FILE: %OUTPUT%


set /P c=ARE YOU SURE TO START ENCODING?[Y/N]?
if /I "%c%" EQU "Y" goto :start
if /I "%c%" EQU "N" goto :setup
goto :setup

:start
echo RUNNING COMMAND
ffmpeg -framerate %FPS% -f image2 -i %PATTERN% -c:v libvpx-vp9 -minrate %MINRATE%k -b:v %MINRATE%k -maxrate %MAXRATE% %OUTPUT%

pause