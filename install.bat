@echo off
Rem Install NodeJS Server
set "current_dir=C:\App"
echo "%current_dir%"
echo "%current_dir%\eAlarm\manager.py"
pause
call nssm-2.21.1\win32\nssm.exe install eAlarmWebapp "C:\Python27\python.exe" "C:\App\eAlarm" "manage.py runserver 0.0.0.0:8000"
sc config eAlarmWebapp start=  auto
call net start eAlarmWebapp
pause
