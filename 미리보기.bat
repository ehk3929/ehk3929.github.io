@echo off
chcp 949 >nul
cd /d "%~dp0"
py preview_launcher.py
if errorlevel 1 pause
