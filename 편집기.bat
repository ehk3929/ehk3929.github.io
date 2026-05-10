@echo off
chcp 949 >nul
cd /d "%~dp0"
py editor_server.py
if errorlevel 1 pause
