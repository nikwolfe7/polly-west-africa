@echo off
tasklist /nh /fi "imagename eq python.exe" | find /i "python.exe" >nul && (
echo Python is running
taskkill /f /im "python.exe"
cd C:\Users\PD\Documents\polly\pythonDongle
start python delayed_requests.py
) || (
echo Python is not running
cd C:\Users\PD\Documents\polly\pythonDongle
start python delayed_requests.py
)
:end