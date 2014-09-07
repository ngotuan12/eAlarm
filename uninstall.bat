@echo off

rem Uninstall NodeJS Server
set "current_dir=C:\App"
call net stop eAlarmWebapp
call "%current_dir%\nssm-2.21.1\win32\nssm.exe" remove eAlarmWebapp 
pause
