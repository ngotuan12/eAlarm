@echo off
Rem Install NodeJS Server
set "current_dir=C:\App\NodeJS"
echo "%current_dir%"
pause
call "%current_dir%\nssm-2.21.1\win32\nssm.exe" install eAlarmSocketServer "%current_dir%\node.exe" "%current_dir%\WebSocket.js"
sc config eAlarmSocketServer start=  auto
call net start eAlarmSocketServer
pause
