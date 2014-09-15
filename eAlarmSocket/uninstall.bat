@echo off

rem Uninstall NodeJS Server
set "current_dir=C:\App\NodeJS"
call net stop eAlarmSocketServer
call "%current_dir%\nssm-2.21.1\win32\nssm.exe" remove eAlarmSocketServer 
pause
