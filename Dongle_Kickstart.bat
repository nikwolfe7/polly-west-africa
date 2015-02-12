@echo off
tasklist /nh /fi "imagename eq Mobile Partner.exe" | find /i "Mobile Partner.exe" >nul && (
echo Mobile Partner is running! Killing...
taskkill /f /im "Mobile Partner.exe"
) 
tasklist /nh /fi "imagename eq python.exe" | find /i "python.exe" >nul && (
echo Python is running
taskkill /f /im "python.exe"
cd C:\Users\PD\Documents\polly\pythonDongle
start python get_call.py
) || (
echo Python is not running
cd C:\Users\PD\Documents\polly\pythonDongle
start python get_call.py
)
:end