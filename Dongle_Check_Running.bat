@echo off
tasklist /nh /fi "imagename eq python.exe" | find /i "python.exe" >nul && (
echo Python is running
) || (
echo Python is not running
cd C:\Users\PD\Documents\polly\pythonDongle
start python get_call.py
)
:end