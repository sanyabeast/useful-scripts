#Requires AutoHotkey v2.0

#h::WinMinimize "A" ; Win+H: Minimize active window
#q::Send "!{F4}" ; Win+Q: Close active window
#Enter::WinMaximize "A" ; Win+Enter: Maximize active window
#!t::Run "wt.exe" ; Win+Alt+T: Launch Windows Terminal